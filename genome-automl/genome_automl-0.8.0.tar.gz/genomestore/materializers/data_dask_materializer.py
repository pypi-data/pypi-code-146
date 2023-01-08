from typing import Mapping, List, Tuple, Dict, Type, Any
from enum import Enum

from ..base import DataRef, Dataset, DataArtifact
from .factory import DataFrameMaterializer, DataFormat, NoFormatSupport

import json
import logging

import dask

MODELSTORE_API = os.getenv('BLOBSTORE') or os.getenv('GENOMESTORE')


class DaskMaterializer(DataFrameMaterializer):

    SUPPORTED_TYPES = (dask.dataframe, )


    def __init__(self):

        super().__init__()



    def load_ref(self, data_type: dask.dataframe,
                       format: DataFormat,
                       data_refs: List[DataRef],
                       options: Dict[str, Any] = None) -> dask.dataframe:

        pass
