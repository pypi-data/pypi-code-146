from logging import Logger
import os
from typing import List, Optional, Union

import numpy as np
import pandas as pd

from truera.client.client_utils import infer_format
from truera.client.client_utils import InvalidInputDataFormat
from truera.client.client_utils import TextExtractorParams
from truera.client.data_source_utils import best_effort_remove_temp_files
from truera.client.data_source_utils import build_static_data_type
from truera.client.truera_workspace_utils import create_temp_file_path
from truera.client.util.data_split.base_data_split_path_container import \
    BaseDataSplitPathContainer
from truera.protobuf.public.common import schema_pb2 as schema_pb
# pylint: disable=no-name-in-module
from truera.protobuf.public.common.schema_pb2 import ColumnDetails
from truera.protobuf.public.util.data_type_pb2 import DataType
from truera.protobuf.public.util.data_type_pb2 import DiscreteIntegerOptions
from truera.protobuf.public.util.data_type_pb2 import DiscreteStringOptions
from truera.protobuf.public.util.data_type_pb2 import StaticDataTypeEnum

# pylint: enable=no-name-in-module

NAN_REP = "NaN"  # how to materialize np.nan in the csv


class PandasDataSplitPathContainer(BaseDataSplitPathContainer):

    def __init__(
        self,
        pre_data: Optional[Union[pd.DataFrame, str]] = None,
        post_data: Optional[Union[pd.DataFrame, str]] = None,
        extra_data: Optional[Union[pd.DataFrame, str]] = None,
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
        prediction_data: Optional[pd.DataFrame] = None,
        feature_influence_data: Optional[pd.DataFrame] = None,
        logger: Logger = None
    ):
        super().__init__(
            pre_data, post_data, extra_data, label_data, prediction_data,
            feature_influence_data
        )
        self.temp_files_to_clean_up_accumulator = []
        self.logger = logger

    def clean_up_temp_files(self):
        best_effort_remove_temp_files(self.temp_files_to_clean_up_accumulator)

    def _get_file_for_upload(
        self, data: Union[pd.DataFrame, str]
    ) -> Optional[Union[pd.DataFrame, str]]:
        if data is None:
            return data
        elif not isinstance(data, (str, pd.DataFrame)):
            raise ValueError(
                f"Provided data was not of a valid type: {type(data)}, "
                "only str and DataFrame are allowed."
            )
        elif isinstance(data, str):
            if not os.path.isfile(data):
                raise ValueError(
                    f"Provided path does not point to a file: {data}"
                )
            return data
        else:
            temp_file_path = create_temp_file_path()
            data.to_csv(
                temp_file_path, index=False, header=True, na_rep=NAN_REP
            )
            self.temp_files_to_clean_up_accumulator.append(temp_file_path)
            return temp_file_path

    def _get_text_extractor_params_for_data(
        self, data: Union[pd.DataFrame, str]
    ) -> TextExtractorParams:
        return TextExtractorParams(
            infer_format("csv", str), True, ",", "\"", "", "",
            TextExtractorParams.DEFAULT_DATE_FORMAT,
            infer_columns_from_df(data, logger=self.logger)
        )


def infer_columns_from_df(
    data: Union[pd.DataFrame, str],
    default_on_failure: bool = False,
    logger: Logger = None
) -> List[schema_pb.ColumnDetails]:
    if isinstance(data, pd.DataFrame):
        columns = pandas_dtypes_to_column_details(
            data.dtypes, default_on_failure=default_on_failure, logger=logger
        )
        return columns
    return TextExtractorParams.DEFAULT_COLUMNS


"""
NOTE: Column schema support is provided for Pandas data types as per
this table: https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes.
The following types from the table are not yet supported and will cause
an exception unless the keyword argument `default_on_failure` is set to `True`:
- PeriodDtype
- SparseDtype
- IntervalDtype
"""


def pandas_dtypes_to_column_details(
    dtypes: pd.Series,
    default_on_failure: bool = False,
    logger: Logger = None
) -> List[schema_pb.ColumnDetails]:
    columns = []
    for name, dtype in dtypes.items():
        try:
            col_data_type = pandas_dtype_to_column_type(dtype, logger=logger)
            columns.append(ColumnDetails(name=name, data_type=col_data_type))
        except ValueError:
            if default_on_failure:
                return TextExtractorParams.DEFAULT_COLUMNS
            raise InvalidInputDataFormat(
                f"Unable to build column schema: column `{name}` is using "
                f"an unsupported data type: `{dtype.name}`."
            )
    return columns


def pandas_dtype_to_column_type(dtype: any, logger: Logger = None) -> DataType:
    type_name = dtype.name.upper()
    if type_name in StaticDataTypeEnum.keys():
        return build_static_data_type(StaticDataTypeEnum.Value(type_name))
    elif type_name == "OBJECT":
        if logger:
            logger.warning(
                f"Converting Pandas object type `{dtype}` to static string type "
                "during schema inference."
            )
        return build_static_data_type(StaticDataTypeEnum.STRING)
    elif type_name == "BOOLEAN":
        return build_static_data_type(StaticDataTypeEnum.BOOL)
    elif type_name == "CATEGORY":
        return build_discrete_options_type_from_category(dtype)
    elif type_name.startswith("DATETIME64"):
        return build_static_data_type(StaticDataTypeEnum.DATETIME)
    else:
        raise ValueError(
            f"Unable to find a valid mapping for Pandas type {type_name}"
        )


def build_discrete_options_type_from_category(
    dtype: pd.CategoricalDtype
) -> DataType:
    category_type_name = dtype.categories.dtype.name
    if category_type_name == 'int64':
        return DataType(
            integer_options_type=DiscreteIntegerOptions(
                possible_values=list(dtype.categories)
            )
        )
    else:
        return DataType(
            string_options_type=DiscreteStringOptions(
                possible_values=list(dtype.categories.astype(str))
            )
        )
