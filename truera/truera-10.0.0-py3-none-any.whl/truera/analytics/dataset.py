from __future__ import annotations

from datetime import datetime
import logging
import os
from typing import (
    Dict, Iterable, List, Mapping, Optional, Sequence, TYPE_CHECKING
)

import numpy as np
import pandas as pd

from truera.analytics.loader.schema_loader import CsvSchemaConfiguration
from truera.protobuf.public.common.schema_pb2 import \
    ColumnDetails  # pylint: disable=no-name-in-module
from truera.protobuf.public.data.data_split_pb2 import \
    DataSplit  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.data_type_pb2 import \
    StaticDataTypeEnum  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.split_mode_pb2 import \
    SplitMode  # pylint: disable=no-name-in-module
from truera.utils.config_util import get_config_value
from truera.utils.datetime_util.datetime_parse_util import \
    get_datetime_from_proto_string
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraNotFoundError

if TYPE_CHECKING:
    from truera.analytics.intelligence_processor import IntelligenceProcessor

STATIC_DATA_TYPE_CONVERSION = {
    StaticDataTypeEnum.STRING:
        str,
    StaticDataTypeEnum.BOOL:
        bool,
    StaticDataTypeEnum.INT8:
        np.int8,
    StaticDataTypeEnum.INT16:
        np.int16,
    StaticDataTypeEnum.INT32:
        np.int32,
    StaticDataTypeEnum.INT64:
        np.int64,
    StaticDataTypeEnum.INTPTR:
        np.intp,
    StaticDataTypeEnum.UINT8:
        np.uint8,
    StaticDataTypeEnum.UINT16:
        np.uint16,
    StaticDataTypeEnum.UINT32:
        np.uint32,
    StaticDataTypeEnum.UINT64:
        np.uint64,
    StaticDataTypeEnum.UINTPTR:
        np.uintp,
    StaticDataTypeEnum.FLOAT32:
        np.float32,
    StaticDataTypeEnum.FLOAT64:
        np.float64,
    StaticDataTypeEnum.DATETIME:
        np.datetime64,
    StaticDataTypeEnum.DATETIME64:
        np.datetime64,
    #StaticDataTypeEnum.COMPLEXFLOAT32: None,
    StaticDataTypeEnum.COMPLEXFLOAT64:
        np.complex64,
    StaticDataTypeEnum.COERCEDBINARY:
        np.int32,
}


class DataTypesHelper:

    @staticmethod
    def get_dtypes_map(columns: List[ColumnDetails]) -> Dict[str, type]:
        # TODO(AB#3334): This doesn't handle integer_options_type and string_options_type.
        return {
            col.name:
            STATIC_DATA_TYPE_CONVERSION[col.data_type.static_data_type]
            for col in columns
            if col.data_type.static_data_type != StaticDataTypeEnum.INVALID
        }


def _check_df_column_type_matches(df: pd.DataFrame):
    logger = logging.getLogger(__name__)
    for column in df.columns:
        column_data = df[column]
        cell_type_series = column_data.apply(type)
        logger.info(cell_type_series)
        if cell_type_series.nunique() == 1:
            continue

        # More than 1 value detected.
        column_dtype = column_data.dtype
        first_value_type = cell_type_series.iloc[0]
        first_nonmatching = cell_type_series.ne(first_value_type).idxmax()
        raise ValueError(
            (
                "Found column '{}' (dtype {}) with mismatched data. First value is '{}' (with type {}), but found nonmatching value '{}' (with type {}) at row {}"
            ).format(
                column, column_data.iloc[0], column_dtype, first_value_type,
                column_data.iloc[first_nonmatching],
                cell_type_series.iloc[first_nonmatching], first_nonmatching
            )
        )
    pass


class DataReader(object):

    def __init__(
        self,
        server_config: dict,
        missing_values: Optional[Sequence[str]] = None
    ):
        if missing_values is None:
            missing_values = []
        self.server_config = server_config
        self.missing_values = missing_values
        self.logger = logging.getLogger(__name__)

    def read_csv(
        self,
        path: str,
        dtypes: Optional[Mapping[str, type]] = None,
        *,
        header_none: bool = False,
        column_names: Optional[List[str]] = None
    ) -> pd.DataFrame:
        data_read_row_limit = self.get_max_rows_to_read()
        kwargs = {}
        if header_none:
            kwargs["header"] = None
        if column_names:
            kwargs["names"] = column_names

        dtypes_no_dates = {}
        date_columns = []
        if dtypes is not None:
            for key in dtypes:
                if dtypes[key] == np.datetime64:
                    date_columns.append(key)
                else:
                    dtypes_no_dates[key] = dtypes[key]

        df = pd.read_csv(
            path,
            keep_default_na=False,
            na_values=self.missing_values,
            nrows=data_read_row_limit,
            dtype=dtypes_no_dates,
            parse_dates=date_columns,
            **kwargs
        )

        if get_config_value(
            self.server_config, "user_data_reader", "enable_fill_na", False
        ):
            str_fill_na = get_config_value(
                self.server_config, "user_data_reader", "fill_na_string_col", ""
            )
            numeric_fill_na = get_config_value(
                self.server_config, "user_data_reader", "fill_na_numeric_col",
                float("NaN")
            )

            columns = list(df.columns)
            dtypes = df.dtypes
            for column in columns:
                is_str_column = dtypes[columns.index(column)] == "object"
                if is_str_column:
                    df[column].fillna(str_fill_na, inplace=True)
                else:
                    df[column].fillna(numeric_fill_na, inplace=True)

        check_type_matches = get_config_value(
            self.server_config, "user_data_reader", "check_column_type_matches",
            False
        )
        if check_type_matches:
            _check_df_column_type_matches(df)

        return df

    def get_max_rows_to_read(self):
        return get_config_value(
            self.server_config, "user_data_reader", "data_read_row_limit", 50000
        )


class Dataset(object):
    """Represents the dataset used to generate a model.
    
    """

    def __init__(
        self,
        dataset_id: str,
        splits: Sequence[DataSplit],
        schema_info: CsvSchemaConfiguration,
        *,
        data_reader: DataReader = DataReader({}),
        project_id: str = 'default',
    ):
        self.logger = logging.getLogger('ailens.Dataset')
        self.dataset_id = dataset_id
        self.project_id = project_id
        self.logger.debug("Creating dataset %s", self.dataset_id)
        self.data_reader = data_reader
        self.schema_info = schema_info
        self._splits: Mapping[str, SplitInfo] = {
            sp.id: SplitInfo(sp, data_reader, schema_info=schema_info)
            for sp in splits
        }
        self._base_split_id: str = ""

    def set_base_split_id(self, base_split_id: str):
        self._base_split_id = base_split_id

    def get_base_split_id(self) -> Optional[str]:
        return self._base_split_id

    def get_split(self, split_id: str) -> Optional['SplitInfo']:
        split_id = split_id or self.get_base_split_id()

        if not split_id:
            return None
        if split_id not in self._splits:
            raise TruEraNotFoundError(
                f"No such split {split_id} in {list(self._splits.keys())}"
            )

        return self._splits[split_id]

    def get_splits(self) -> Sequence['SplitInfo']:
        """gets a list of splits"""

        return self._splits.values()

    def remove_split(self, id):
        if id not in self._splits:
            self.logger.warning(
                "Trying to delete non-existent split %s from dataset %s", id,
                self.dataset_id
            )
            return
        del self._splits[id]

    def add_split(self, split: DataSplit):
        if split.id in self._splits:
            raise ValueError(
                'Tried to add duplicate split {} to dataset {}'.format(
                    split.id, self.dataset_id
                )
            )
        self._splits[split.id
                    ] = SplitInfo(split, self.data_reader, self.schema_info)


class SplitInfo:

    def __init__(
        self, proto: DataSplit, data_reader: DataReader,
        schema_info: CsvSchemaConfiguration
    ):
        self.logger = logging.getLogger(__name__)
        self.proto = proto
        self._set_last_updated_on()
        self.data_reader = data_reader
        self.feature_list = schema_info
        self._preprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.pre_schema
        )
        self._postprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.post_schema
        )
        self._extraprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.extra_schema
        )
        self._labelprocessed_dtypes = DataTypesHelper.get_dtypes_map(
            schema_info.label_schema
        )

        # system data may include system ID cols, timestamp cols, etc. that should be ignored for analytics
        self._preprocessed_data_with_system_data: Optional[pd.DataFrame] = None
        self._processed_data_with_system_data: Optional[pd.DataFrame] = None
        self._label_with_system_data: Optional[pd.DataFrame] = None
        self._extra_data_with_system_data: Optional[pd.DataFrame] = None
        self._label_column_name: Optional[str] = None

        self.split_id = proto.id
        self.split_name = proto.name
        self.split_type = proto.split_type
        self.split_mode = proto.split_mode

        self._loaded = False
        self._is_valid: Optional[bool] = None
        self._validation_exception = None

    def _set_last_updated_on(self):
        self.updated_on = get_datetime_from_proto_string(self.proto.updated_on)

    @property
    def num_inputs(self) -> int:
        if self.split_mode == SplitMode.SPLIT_MODE_PREDS_REQUIRED:
            # NB: We are assuming here that full labels are provided and that they are always aligned to predictions.
            return len(self.label_data)
        return len(self.preprocessed_data)

    @property
    def feature_names(self) -> Iterable[str]:
        return list(self.preprocessed_data.columns)

    @property
    def processed_feature_names(self) -> Iterable[str]:
        return list(self.processed_data.columns)

    @property
    def pre_transform_locator(self) -> str:
        return self.proto.preprocessed_locator

    @property
    def post_transform_locator(self) -> str:
        return self.proto.processed_locator

    @property
    def label_locator(self) -> str:
        return self.proto.label_locator

    @property
    def unique_id_column_name(self) -> str:
        return self.proto.unique_id_column_name

    @property
    def timestamp_column_name(self) -> str:
        return self.proto.timestamp_column_name

    @property
    def label_column_name(self) -> str:
        self._read_label_data_if_needed()
        return self._label_column_name

    @property
    def system_column_names(self) -> Sequence[str]:
        return [
            col
            for col in [self.unique_id_column_name, self.timestamp_column_name]
            if col
        ]

    def _read_preprocessed_data_if_needed(self):
        if self.proto.preprocessed_locator and self._preprocessed_data_with_system_data is None:
            self._preprocessed_data_with_system_data = self.data_reader.read_csv(
                self.proto.preprocessed_locator, self._preprocessed_dtypes
            )
            if self.unique_id_column_name:
                self._preprocessed_data_with_system_data.set_index(
                    self.unique_id_column_name, inplace=True
                )

    def _read_processed_data_if_needed(self):
        if self._processed_data_with_system_data is None and self.proto.processed_locator and os.path.exists(
            self.proto.processed_locator
        ):
            self._processed_data_with_system_data = self.data_reader.read_csv(
                self.proto.processed_locator, self._postprocessed_dtypes
            )
            if self.unique_id_column_name:
                self._processed_data_with_system_data.set_index(
                    self.unique_id_column_name, inplace=True
                )
        self.validate_processed_data()

    def _read_label_data_if_needed(self):
        if self._label_with_system_data is None and self.proto.label_locator and os.path.exists(
            self.proto.label_locator
        ):
            # This is done temporarily to support label file with and without header
            # for backward compatibility.
            if "__internal_with_headers" in os.path.basename(
                self.proto.label_locator
            ):
                self._label_with_system_data = self.data_reader.read_csv(
                    self.proto.label_locator, self._labelprocessed_dtypes
                )
                unaccounted_cols = [
                    col for col in self._label_with_system_data.columns
                    if col not in self.system_column_names
                ]
                if len(unaccounted_cols) > 1:
                    raise TruEraInternalError(
                        f"Label data has unrecognized columns {unaccounted_cols}!"
                    )
                self._label_column_name = unaccounted_cols[0]
                if self.unique_id_column_name:
                    self._label_with_system_data.set_index(
                        self.unique_id_column_name, inplace=True
                    )
                self._label_with_system_data = self._label_with_system_data.reindex(
                    self.processed_or_preprocessed_data_with_system_data.index
                )
            else:
                # assume labels without headers are one-column CSVs, and assign a header to them
                self._label_column_name = "ground_truth"
                self._label_with_system_data = self.data_reader.read_csv(
                    self.proto.label_locator,
                    self._labelprocessed_dtypes,
                    header_none=True,
                    column_names=[self._label_column_name]
                )
        # TODO(AB#6242): Consider delayed labels scenario for monitoring superlite.
        self.validate_labels()

    def _read_extra_data_if_needed(self):
        if self._extra_data_with_system_data is None and self.proto.extra_data_locator and os.path.exists(
            self.proto.extra_data_locator
        ):
            self._extra_data_with_system_data = self.data_reader.read_csv(
                self.proto.extra_data_locator, self._extraprocessed_dtypes
            )
            if self.unique_id_column_name:
                self._extra_data_with_system_data.set_index(
                    self.unique_id_column_name, inplace=True
                )
        self.validate_extra_data()

    @property
    def preprocessed_data_with_system_data(self) -> pd.DataFrame:
        self._read_preprocessed_data_if_needed()
        return self._preprocessed_data_with_system_data

    @property
    def preprocessed_data(self) -> pd.DataFrame:
        if self.timestamp_column_name:
            return self.preprocessed_data_with_system_data.drop(
                self.timestamp_column_name, axis="columns"
            )
        return self.preprocessed_data_with_system_data

    @property
    def processed_data_with_system_data(self) -> pd.DataFrame:
        self._read_processed_data_if_needed()
        return self._processed_data_with_system_data

    @property
    def processed_data(self) -> pd.DataFrame:
        if self.timestamp_column_name and self.processed_data_with_system_data is not None:
            return self.processed_data_with_system_data.drop(
                self.timestamp_column_name, axis="columns"
            )
        return self.processed_data_with_system_data

    @property
    def label_data_with_system_data(self) -> pd.DataFrame:
        self._read_label_data_if_needed()
        return self._label_with_system_data

    @property
    def label_data(self) -> pd.DataFrame:
        if self.timestamp_column_name and self.label_data_with_system_data is not None:
            return self.label_data_with_system_data.drop(
                self.timestamp_column_name, axis="columns"
            )
        return self.label_data_with_system_data

    @property
    def extra_data_with_system_data(self) -> pd.DataFrame:
        self._read_extra_data_if_needed()
        return self._extra_data_with_system_data

    @property
    def extra_data(self) -> pd.DataFrame:
        if self.timestamp_column_name and self.extra_data_with_system_data is not None:
            return self.extra_data_with_system_data.drop(
                self.timestamp_column_name, axis="columns"
            )
        return self.extra_data_with_system_data

    @property
    def has_labels(self) -> bool:
        return self.label_data is not None

    @property
    def processed_or_preprocessed_data(self) -> pd.DataFrame:
        return self.processed_data if self.processed_data is not None else self.preprocessed_data

    @property
    def processed_or_preprocessed_data_with_system_data(self) -> pd.DataFrame:
        return self.processed_data_with_system_data if self.processed_data_with_system_data is not None else self.preprocessed_data_with_system_data

    def validate_processed_data(self):
        if self._processed_data_with_system_data is not None and self.preprocessed_data_with_system_data is not None and len(
            self._processed_data_with_system_data
        ) != len(self.preprocessed_data_with_system_data):
            raise TruEraInternalError(
                f"Data mismatch in split {self.split_id}! Preprocessed data has {len(self.preprocessed_data_with_system_data)} rows. Postprocessed data has {len(self._processed_data_with_system_data)} rows."
            )

    def validate_extra_data(self):
        if self._extra_data_with_system_data is not None and self.preprocessed_data_with_system_data is not None and len(
            self._extra_data_with_system_data
        ) != len(self.preprocessed_data_with_system_data):
            raise TruEraInternalError(
                f"Data mismatch in split {self.split_id}! Preprocessed data has {len(self.preprocessed_data_with_system_data)} rows. Extra data has {len(self._extra_data_with_system_data)} rows."
            )

    def validate_labels(self):
        if self.unique_id_column_name or self._label_with_system_data is None or self.preprocessed_data_with_system_data is None:
            return
        if len(self._label_with_system_data
              ) != len(self.preprocessed_data_with_system_data):
            raise TruEraInternalError(
                f"Data mismatch in split {self.split_id}! Preprocessed data has {len(self.preprocessed_data_with_system_data)} rows. Labels have {len(self._label_with_system_data)} rows."
            )
