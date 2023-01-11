from __future__ import annotations

from datetime import datetime
from enum import Enum
import logging
import os
from os.path import splitext
import platform
from time import sleep
from typing import Any, Callable, List, Mapping, Optional, Sequence, Tuple

from google.protobuf.timestamp_pb2 import \
    Timestamp  # pylint: disable=no-name-in-module

from truera.client.errors import NotFoundError
from truera.client.errors import SimpleException
from truera.client.errors import TruException
from truera.protobuf.public import metadata_message_types_pb2 as md_pb
from truera.protobuf.public import qoi_pb2 as qoi_pb
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as ds_messages_pb
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.protobuf.public.util import time_range_pb2 as tr_pb
from truera.public.feature_influence_constants import \
    ALL_CLASSIFICATION_SCORE_TYPES
from truera.public.feature_influence_constants import \
    ALL_REGRESSION_SCORE_TYPES
from truera.public.feature_influence_constants import \
    VALID_SCORE_TYPES_FOR_CLASSIFICATION
from truera.public.feature_influence_constants import \
    VALID_SCORE_TYPES_FOR_REGRESSION
from truera.utils import filter_constants


class InvalidInputDataFormat(TruException):
    pass


class DataOperationFailedError(TruException):
    pass


class DataOperationPendingError(TruException):
    pass


class TextFormatNotSupportedError(SimpleException):
    pass


class InvalidQuantityOfInterestError(SimpleException):
    pass


class InvalidArgumentCombinationException(SimpleException):
    pass


class BadTimestampException(SimpleException):
    pass


_STRING_TO_QOI = {
    "logits":
        qoi_pb.QuantityOfInterest.LOGITS_SCORE,
    "probits":
        qoi_pb.QuantityOfInterest.PROBITS_SCORE,
    "classification":
        qoi_pb.QuantityOfInterest.CLASSIFICATION_SCORE,
    "regression":
        qoi_pb.QuantityOfInterest.REGRESSION_SCORE,
    "log_loss":
        qoi_pb.QuantityOfInterest.LOG_LOSS,
    "mean_absolute_error_for_classification":
        qoi_pb.QuantityOfInterest.MEAN_ABSOLUTE_ERROR_FOR_CLASSIFICATION,
    "mean_absolute_error_for_regression":
        qoi_pb.QuantityOfInterest.MEAN_ABSOLUTE_ERROR_FOR_REGRESSION,
}

_QOI_TO_STRING = {qoi: string for string, qoi in _STRING_TO_QOI.items()}

_QOI_NAME_TO_SCORE_TYPE = {
    "LOGITS_SCORE": "logits",
    "PROBITS_SCORE": "probits",
    "CLASSIFICATION_SCORE": "classification",
    "REGRESSION_SCORE": "regression",
}
# Technically the backend supports creating a project with 'unknown_input_data' and 'image' as  input data format,
# however we should not surface them in the  python client since unknown is there only for backward
# compatibility,  and 'image' is currently not supported  at all by the rest of the product.
# TODO: include 'image' when the product supports it.
_STRING_TO_INPUT_DATA_FORMAT = {
    i[0].lower(): i[1] for i in md_pb.InputDataFormat.items()
}
_STRING_TO_INPUT_DATA_FORMAT.pop('unknown_input_format')
_STRING_TO_INPUT_DATA_FORMAT.pop('image')

_STRING_TO_MODEL_TYPE = {i[0].lower(): i[1] for i in md_pb.ModelType.items()}


def get_input_data_format_from_string(input_data_format: str):
    if input_data_format.lower() not in _STRING_TO_INPUT_DATA_FORMAT:
        raise InvalidInputDataFormat(
            f"\"{input_data_format}\" is not a valid input data type! Must be one of {list(_STRING_TO_INPUT_DATA_FORMAT.keys())}."
        )
    return _STRING_TO_INPUT_DATA_FORMAT[input_data_format.lower()]


def get_model_type_from_string(model_type: str) -> md_pb.ModelType:
    if model_type.lower() not in _STRING_TO_MODEL_TYPE:
        raise InvalidInputDataFormat(
            f"\"{model_type}\" is not a valid model type! Must be one of {list(_STRING_TO_MODEL_TYPE.keys())}."
        )
    return _STRING_TO_MODEL_TYPE[model_type.lower()]


def get_explanation_algorithm_type_from_string(
    algorithm_type: str
) -> qoi_pb.ExplanationAlgorithmType:
    if algorithm_type.lower() not in STR_TO_EXPLANATION_ALGORITHM_TYPE:
        raise InvalidInputDataFormat(
            f"\"{algorithm_type}\" is not a valid explanation algorithm type! Must be one of "
            f"{list(STR_TO_EXPLANATION_ALGORITHM_TYPE.keys())}."
        )
    return STR_TO_EXPLANATION_ALGORITHM_TYPE[algorithm_type.lower()]


def get_qoi_from_string(score_type: str) -> qoi_pb.QuantityOfInterest:
    if score_type.lower() not in _STRING_TO_QOI:
        raise InvalidQuantityOfInterestError(
            "Provided score type was invalid: " + score_type
        )
    return _STRING_TO_QOI[score_type.lower()]


def get_string_from_qoi(qoi: qoi_pb.QuantityOfInterest) -> str:
    if qoi not in _QOI_TO_STRING:
        raise InvalidQuantityOfInterestError(
            f"Provided quantity of interest was invalid: {qoi} not in {_QOI_TO_STRING}"
        )
    return _QOI_TO_STRING[qoi]


def get_string_from_qoi_string(qoi_str: str):
    if qoi_str not in _QOI_NAME_TO_SCORE_TYPE:
        raise InvalidQuantityOfInterestError(
            "Provided quantity of interest was invalid: " + qoi_str
        )
    return _QOI_NAME_TO_SCORE_TYPE[qoi_str]


def get_context_storage_base_path():
    if platform.system().lower() == "windows":
        home_path = os.path.join(
            os.environ["HOMEDRIVE"], os.environ["HOMEPATH"]
        )
        user_profile = os.environ["USERPROFILE"]

        base_dir = None
        if os.path.isdir(home_path):
            base_dir = home_path
        elif os.path.isdir(user_profile):
            base_dir = user_profile
        else:
            print(
                f"Warning: Could not determine base_dir from %HOMEDRIVE%\%HOMEPATH% ({home_path}) or from %USERPROFILE% ({user_profile})."
            )
            print(f"Warning: Trying %SYSTEMDRIVE%:\%HOMEPATH%...")
            base_dir = os.path.join(
                os.environ["SYSTEMDRIVE"], os.environ["HOMEPATH"]
            )
            if not os.path.isdir(base_dir):
                message = f"%SYSTEMDRIVE%\%HOMEPATH% ({base_dir}) does not exist. Please set %USERPROFILE% to a drive that exists."
                print(f"Error: {message}")
                raise ContextSetupException(message)
        return os.path.join(base_dir, "Truera")
    else:
        return os.path.join(os.environ["HOME"], ".truera")


class ContextSetupException(SimpleException):
    pass


class NotSupportedFileTypeException(SimpleException):
    pass


class VersionMismatchError(SimpleException):
    pass


def get_current_version(logger=None):
    logger = logger if logger else logging.getLogger(__name__)
    cli_version_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "cli", "cli_version.txt"
    )
    with open(cli_version_path) as f:
        return f.read()


def check_version_up_to_date(server_side_cli_version, logger=None):
    logger = logger if logger else logging.getLogger(__name__)
    client_side_cli_version = get_current_version(logger)

    comparison_result = _compare_versions(
        server_side_cli_version, client_side_cli_version
    )

    if comparison_result == VersionComparisonResult.BAD_FORMAT:
        logger.warning(
            f"Warning: Something went wrong checking cli version. Server version: {server_side_cli_version}, client version {client_side_cli_version}."
        )
    elif comparison_result == VersionComparisonResult.ERROR_OUT_OF_DATE:
        message = (
            f"Error: Tru client is out of date on major version. "
            f"Please update the client before use. "
            f"Server version: {server_side_cli_version}, client version {client_side_cli_version}."
        )
        logger.error(message)
        raise VersionMismatchError(message)
    elif comparison_result == VersionComparisonResult.ERROR_CLIENT_VERSION_NEWER_THAN_SERVER:
        message = (
            f"Error: Tru client is newer than server version. "
            f"Please install the client from the server you are trying to connect. "
            f"Server version: {server_side_cli_version}, client version {client_side_cli_version}."
        )
        logger.error(message)
        raise VersionMismatchError(message)
    elif comparison_result == VersionComparisonResult.WARN_OUT_OF_DATE:
        logger.warning(
            f"Warning: Tru client is out of date. Upgrade is recommended. Server side: {server_side_cli_version}, client side {client_side_cli_version}."
        )


class VersionComparisonResult(Enum):
    OK = "OK"
    BAD_FORMAT = "BAD_FORMAT"
    ERROR_OUT_OF_DATE = "ERROR_OUT_OF_DATE"
    WARN_OUT_OF_DATE = "WARN_OUT_OF_DATE"
    ERROR_CLIENT_VERSION_NEWER_THAN_SERVER = "ERROR_CLIENT_VERSION_NEWER_THAN_SERVER"


def _compare_versions(
    server_side_cli_version, client_side_cli_version
) -> VersionComparisonResult:
    server_side_cli_version_parts = server_side_cli_version.split('.')
    client_side_cli_version_parts = client_side_cli_version.split('.')

    if len(server_side_cli_version_parts
          ) != 3 or len(client_side_cli_version_parts) != 3:

        return VersionComparisonResult.BAD_FORMAT

    server_major, server_minor, server_patch = int(
        server_side_cli_version_parts[0]
    ), int(server_side_cli_version_parts[1]
          ), int(server_side_cli_version_parts[2])
    client_major, client_minor, client_patch = int(
        client_side_cli_version_parts[0]
    ), int(client_side_cli_version_parts[1]
          ), int(client_side_cli_version_parts[2])

    if server_major < client_major:
        return VersionComparisonResult.ERROR_CLIENT_VERSION_NEWER_THAN_SERVER
    if server_major == client_major and server_minor < client_minor:
        return VersionComparisonResult.ERROR_CLIENT_VERSION_NEWER_THAN_SERVER
    if server_major > client_major:
        return VersionComparisonResult.ERROR_OUT_OF_DATE
    if server_minor > client_minor:
        return VersionComparisonResult.WARN_OUT_OF_DATE

    return VersionComparisonResult.OK


def rowset_status_to_str(status):
    if status == ds_messages_pb.RowsetStatus.RS_STATUS_STARTED:
        return "STARTED"
    if status == ds_messages_pb.RowsetStatus.RS_STATUS_OK:
        return "OK"
    if status == ds_messages_pb.RowsetStatus.RS_STATUS_FAILED:
        return "FAILED"
    return "INVALID"


def materialize_status_to_str(status):
    if status == ds_messages_pb.MaterializeStatus.MATERIALIZE_STATUS_PREPARING:
        return "PREPARING"
    if status == ds_messages_pb.MaterializeStatus.MATERIALIZE_STATUS_RUNNING:
        return "RUNNING"
    if status == ds_messages_pb.MaterializeStatus.MATERIALIZE_STATUS_SUCCEDED:
        return "OK"
    if status == ds_messages_pb.MaterializeStatus.MATERIALIZE_STATUS_FAILED:
        return "FAILED"
    return "INVALID"


def infer_format(specified_format, uri):
    if specified_format.lower() != "infer":
        return specified_format
    _, file_extension = splitext(uri)
    file_extension = file_extension.lstrip(".")

    supported = ["csv", "parquet"]

    for fmt in supported:
        if file_extension.lower() == fmt:
            return fmt

    raise TextFormatNotSupportedError(
        "Could not figure out the file type based on extension. "
        "Supported types: %s. You could also provide the "
        "the format by using the `format` parameter." % supported
    )


class TextExtractorParams:

    DEFAULT_FIRST_ROW_IS_HEADER = True
    DEFAULT_COLUMN_DELIMITER = ","
    DEFAULT_QUOTE_CHARACTER = "\""
    DEFAULT_NULL_VALUE = "null"
    DEFAULT_EMPTY_VALUE = "\"\""
    DEFAULT_DATE_FORMAT = "yyyy-MM-dd HH:mm:ssZZ"
    DEFAULT_COLUMNS = []

    def __init__(
        self, format_type, first_row_is_header, column_delimiter,
        quote_character, null_value, empty_value, date_format, columns
    ):
        super().__init__()
        self.format_type = format_type
        self.first_row_is_header = first_row_is_header if first_row_is_header is not None else TextExtractorParams.DEFAULT_FIRST_ROW_IS_HEADER
        self.column_delimiter = column_delimiter if column_delimiter is not None else TextExtractorParams.DEFAULT_COLUMN_DELIMITER
        self.quote_character = quote_character if quote_character is not None else TextExtractorParams.DEFAULT_QUOTE_CHARACTER
        self.null_value = null_value if null_value is not None else TextExtractorParams.DEFAULT_NULL_VALUE
        self.empty_value = empty_value if empty_value is not None else TextExtractorParams.DEFAULT_EMPTY_VALUE
        self.date_format = date_format if date_format is not None else TextExtractorParams.DEFAULT_DATE_FORMAT
        self.columns = columns if columns is not None else TextExtractorParams.DEFAULT_COLUMNS

    def to_format_pb(self) -> ds_messages_pb.Format:
        if self.format_type.lower() == "csv" or self.format_type.lower(
        ) == "text":
            return ds_messages_pb.Format(
                file_type=ds_messages_pb.FileType.FT_TEXT,
                delimited_format=ds_messages_pb.FormatOptions(
                    first_row_is_header=self.first_row_is_header,
                    column_delimiter=self.column_delimiter,
                    quote_character=self.quote_character,
                    null_value=self.null_value,
                    empty_value=self.empty_value,
                    date_format=self.date_format
                ),
                columns=self.columns
            )
        if self.format_type.lower() == "parquet":
            return ds_messages_pb.Format(
                file_type=ds_messages_pb.FileType.FT_PARQUET,
                columns=self.columns
            )
        if self.format_type.lower() == "sagemaker_monitoring_log":
            return ds_messages_pb.Format(
                file_type=ds_messages_pb.FileType.FT_SAGEMAKER_MONITORING_LOG,
                columns=self.columns
            )


def create_format_pb_from_format_type(
    format_type: str, columns=None
) -> ds_messages_pb.Format:
    text_extractor_params = TextExtractorParams(
        format_type=format_type,
        first_row_is_header=None,
        column_delimiter=None,
        quote_character=None,
        null_value=None,
        empty_value=None,
        date_format=None,
        columns=columns
    )
    return text_extractor_params.to_format_pb()


def create_time_range(time_range_begin: str, time_range_end: str):
    if time_range_begin and time_range_end:
        begin_timestamp = Timestamp()
        end_timestamp = Timestamp()
        try:
            begin_timestamp.FromJsonString(time_range_begin)
            end_timestamp.FromJsonString(time_range_end)
        except ValueError as e:
            raise BadTimestampException(
                f"Time stamp conversion did not succeed. Provided time stamps were begin: {time_range_begin} and end: {time_range_end}. Please make sure the time stamp conforms to RFC 3339 format. Examples of accepted format: 2020-01-01T10:00:20.021-05:00 or 2021-06-03T00:00:00Z."
            )
        return tr_pb.TimeRange(begin=begin_timestamp, end=end_timestamp)
    elif time_range_begin or time_range_end:
        raise InvalidArgumentCombinationException(
            f"Only one of timerange begin / end set. Begin: {time_range_begin}. End: {time_range_end}."
        )
    else:
        return tr_pb.TimeRange()


def wait_for_status(
    logger,
    status_lambda: Callable,
    success_state: str,
    running_states: List[str],
    failed_state: str,
    timeout_seconds: int = 300,
    error_on_timeout: bool = False,
    wait_duration_in_seconds: int = 5
) -> str:
    """

    Args:
        status_lambda (Callable): Function to check the status. This must return a tuple (status, error).
        success_state (str): Value to check for to determine success.
        running_states (List[str]): Value(s) to check for to determine if operation is processing.
        failed_state (str): Value to check for to determine failure.
        timeout_seconds (int, optional): Operation timeout in seconds. Defaults to 300.
        error_on_timeout (bool, optional): Determines whether to throw an error on timeout. Defaults to False.

    Raises:
        DataOperationPendingError: Raised if timeout is reached and error_on_timeout is set.
        DataOperationFailedError: Raised if the operation enters a failed or unknown state.

    Returns:
        str: The final value of status.
    """
    start_time = datetime.now()
    while True:
        status, error = status_lambda()
        if status == success_state:
            return status
        elif status in running_states:
            if (datetime.now() - start_time).seconds <= timeout_seconds:
                logger.debug("Table status is pending, retrying...")
                sleep(wait_duration_in_seconds)
                continue
            elif error_on_timeout:
                # Devnote - we could make these more general if we start using this for other status types
                raise DataOperationPendingError(
                    f"Operation is still being processed.  Please retry later or set a longer timeout."
                )
            else:
                return status
        elif status == failed_state:
            assert error, "TruEra Internal Error: Table is in failed state but client could not retrieve the error."
            # Devnote - we could make these more general if we start using this for other status types
            raise DataOperationFailedError(
                f"Operation is in a failed state. Cause: {error}"
            )
        else:
            # Devnote - we could make these more general if we start using this for other status types
            raise DataOperationFailedError(
                f"Operation is in an unknown state: {status}"
            )


def validate_feature_names(
    feature_names: Sequence[str],
    valid_feature_names: Sequence[str],
    score_type: str,
    allow_label_or_model_column: bool = False
) -> None:
    special_column_names = set()
    if allow_label_or_model_column:
        special_column_names.add(filter_constants.FILTER_GROUND_TRUTH_NAME)
        if score_type in ALL_CLASSIFICATION_SCORE_TYPES:
            special_column_names.update(
                filter_constants.
                CLASSIFICATION_SCORE_TYPES_TO_FILTER_MODEL_OUTPUT_NAMES.values()
            )
        elif score_type in ALL_REGRESSION_SCORE_TYPES:
            special_column_names.update(
                filter_constants.
                REGRESSION_SCORE_TYPES_TO_FILTER_MODEL_OUTPUT_NAMES.values()
            )
    if not feature_names:
        return
    for feature_name in feature_names:
        if not (
            feature_name in valid_feature_names or
            feature_name in special_column_names
        ):
            if allow_label_or_model_column:
                raise ValueError(
                    f"Feature \"{feature_name}\" does not exist. Valid feature names: {valid_feature_names}. Valid special column names: {special_column_names}."
                )
            else:
                raise ValueError(
                    f"Feature \"{feature_name}\" does not exist in this data split!"
                )


def validate_model_metadata(
    train_split_name: Optional[str] = None,
    existing_split_names: Optional[Sequence[str]] = None,
    train_parameters: Optional[Mapping[str, Any]] = None,
    logger: Optional[logging.Logger] = None,
):
    logger = logger if logger else logging.getLogger(__name__)
    if train_split_name:
        if existing_split_names is None:
            raise ValueError(
                f"Please provide `existing_split_names` to validate `train_split_name`."
            )
        if not train_split_name in existing_split_names:
            raise NotFoundError(
                f"Data split with name \"{train_split_name}\" does not exist in data collection."
            )

    if train_parameters:
        if not isinstance(train_parameters, Mapping):
            raise ValueError(
                f"`train_parameters` should be `Mapping[str, str]`"
            )
        for key in train_parameters:
            if not isinstance(key, str):
                raise ValueError(
                    f"All keys of `train_parameters` should be a string. Type of key \"{key}\" is {type(key)}"
                )


def validate_add_model_metadata(
    model_name: str,
    train_split_name: Optional[str] = None,
    existing_train_split_name: Optional[str] = None,
    train_parameters: Optional[Mapping[str, Any]] = None,
    existing_train_parameters: Optional[Mapping[str, Any]] = None,
    overwrite: bool = False
) -> None:
    if overwrite:
        return
    if (
        existing_train_split_name and train_split_name
    ) and existing_train_split_name != train_split_name:
        raise ValueError(
            f"`train_split_name` is already defined for model \"{model_name}\": \"{existing_train_split_name}\". Set `overwrite=True` to overwrite."
        )
    if (
        existing_train_parameters and train_parameters
    ) and existing_train_parameters != train_parameters:
        raise ValueError(
            f"`train_parameters` is already defined for model \"{model_name}\": \"{existing_train_parameters}\". Set `overwrite=True` to overwrite."
        )


STR_TO_EXPLANATION_ALGORITHM_TYPE = {
    "truera-qii":
        ExplanationAlgorithmType.TRUERA_QII,
    "tree-shap-tree-path-dependent":
        ExplanationAlgorithmType.TREE_SHAP_PATH_DEPENDENT,
    "tree-shap-interventional":
        ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL,
    "kernel-shap":
        ExplanationAlgorithmType.KERNEL_SHAP,
    "integrated-gradients":
        ExplanationAlgorithmType.INTEGRATED_GRADIENTS
}

EXPLANATION_ALGORITHM_TYPE_TO_STR = {
    v: k for k, v in STR_TO_EXPLANATION_ALGORITHM_TYPE.items()
}
