from typing import Mapping, List, Tuple, Dict, Type, Any
from enum import Enum

from ..base import DataRef, Dataset, DataArtifact
from .factory import DataFrameMaterializer, DataFormat, NoFormatSupport

import json
import logging

import pandas as pd

MODELSTORE_API = os.getenv('BLOBSTORE') or os.getenv('GENOMESTORE')


class PandasMaterializer(DataFrameMaterializer):

    SUPPORTED_TYPES = (pd.DataFrame, )


    def __init__(self):

        super().__init__()


    def load_ref(self, data_type: Type[Any],
                       format: DataFormat,
                       data_refs: List[DataRef],
                       options: Dict[str, Any] = None) -> pd.DataFrame:


        if DataFormat.JSON == format:
            return pd.concat((pd.read_json(data_ref.ref, storage_options = options) for data_ref in data_refs))


        elif DataFormat.CSV == format:
            return pd.concat((pd.read_csv(data_ref.ref, storage_options = options) for data_ref in data_refs))


        elif DataFormat.PARQUET == format:
            return pd.concat((pd.read_parquet(data_ref.ref, storage_options = options) for data_ref in data_refs))


        else:
            raise NoFormatSupport(
              f"no format support for: {format} by materializer: {type(self).__name__}"
            )





    def save_to_ref(self, dataframe: pd.DataFrame,
                          format: DataFormat,
                          data_ref: DataRef,
                          options: Dict[str, Any] = None) -> None:

        if DataFormat.JSON == format:
            dataframe.to_json(data_ref.ref, storage_options = options)


        elif DataFormat.CSV == format:
            dataframe.to_csv(data_ref.ref, storage_options = options)


        elif DataFormat.PARQUET == format:
            dataframe.to_parquet(data_ref.ref, storage_options = options)
