import os
from typing import List, Tuple, Union

from google.protobuf.json_format import ParseDict

from truera.client.client_pb_utils import load_dict_from_file
from truera.client.client_utils import InvalidInputDataFormat
from truera.protobuf.public.common import schema_pb2 as schema_pb
from truera.protobuf.public.common.data_kind_pb2 import \
    DataKindDescribed  # pylint: disable=no-name-in-module
from truera.protobuf.public.common.schema_pb2 import \
    ColumnDetails  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.data_type_pb2 import \
    DataType  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.data_type_pb2 import \
    StaticDataTypeEnum  # pylint: disable=no-name-in-module


def build_static_data_type(static_data_type: StaticDataTypeEnum) -> DataType:
    return DataType(static_data_type=static_data_type)


def column_to_static_column_details(
    column_name: str, column_data_type: str
) -> schema_pb.ColumnDetails:
    if not isinstance(column_name, str):
        raise InvalidInputDataFormat(
            "Invalid type provided for `column_name` parameter. Expected type "
            f"`str` but received {type(column_name)}"
        )
    if not isinstance(column_data_type, str):
        raise InvalidInputDataFormat(
            "Invalid type provided for `column_data_type` parameter. Expected type "
            f"`str` but received {type(column_data_type)}"
        )

    try:
        return schema_pb.ColumnDetails(
            name=column_name,
            data_type=build_static_data_type(
                StaticDataTypeEnum.Value(column_data_type.upper())
            )
        )
    except ValueError:
        raise InvalidInputDataFormat(
            f"Unrecognized static data type `{column_data_type}` for column "
            f"with name `{column_name}`."
        )


def get_column_details_for_data_source(
    columns: Union[str, List[Tuple[str, str]]]
) -> List[schema_pb.ColumnDetails]:
    if not columns:
        return []

    typ = type(columns)
    if typ is str:
        return get_column_details_from_file(columns)
    elif typ is list:
        return get_column_details_from_list(columns)
    else:
        raise InvalidInputDataFormat(
            "Unsupported input format for column schema. Expected string "
            f"or list but received {typ}"
        )


def get_column_details_from_list(
    column_list: List[Tuple[str, str]]
) -> List[schema_pb.ColumnDetails]:
    columns = map(
        lambda col: column_to_static_column_details(col[0], col[1]), column_list
    )
    return list(columns)


def get_column_details_from_file(file: str) -> List[schema_pb.ColumnDetails]:
    columns_dict = load_dict_from_file(file)
    columns = []
    for column in columns_dict['columns']:
        new_column_details = ColumnDetails()
        ParseDict(column, new_column_details)
        columns.append(new_column_details)
    return columns


def best_effort_remove_temp_files(files_to_delete):
    for file_name in files_to_delete:
        try:
            if file_name:
                os.remove(file_name)
        except:
            pass


DATA_SOURCE_NAME_TO_DATA_KIND = {
    "pre": DataKindDescribed.DATA_KIND_PRE,
    "post": DataKindDescribed.DATA_KIND_POST,
    "extra": DataKindDescribed.DATA_KIND_EXTRA,
    "label": DataKindDescribed.DATA_KIND_LABEL,
    "prediction": DataKindDescribed.DATA_KIND_PREDICTIONS,
    "feature_influence": DataKindDescribed.DATA_KIND_FEATURE_INFLUENCES
}
