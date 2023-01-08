from typing import Mapping, List, Tuple, Dict, Type, Union, Any
from enum import Enum

from ..base import BaseRef, DataRef, Dataset, DataArtifact, ModelArtifact
from .factory import ModelMaterializer, DataFrameMaterializer, DataFormat, NoFormatSupport

import json
import logging
import sys
import time
import os
import os.path
import pickle
import urllib.request
from urllib.error import  URLError
import base64
import io
import glob
import tempfile
import zipfile
import shutil

import warnings


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

try:
    from sklearn.base import BaseEstimator
except ImportError:
    warnings.warn('sklearn could not be imported', ImportWarning)


MODELSTORE_API = os.getenv('BLOBSTORE') or os.getenv('GENOMESTORE')


class SklearnModelMaterializer(ModelMaterializer):

    SUPPORTED_TYPES = (BaseEstimator, )


    def __init__(self):
        super().__init__()


    def load_ref(self, data_type: Type[Any],
                       format: DataFormat,
                       blob_refs: List[BaseRef],
                       options: Dict[str, Any] = None) -> BaseEstimator:


        blobstore_api: str = options["blob_api"] if options and "blob_api" in options else MODELSTORE_API

        blob_ref = blob_refs[0] if len(blob_refs) else None


        # we are assuming we always load model files from the genome blob store
        response = urllib.request.urlopen(blobstore_api + "/v1.0/genome/blob/" + blob_ref.ref)
        model_file = response.read()


        logging.info("initializing sklearn model from blob_ref:" + blob_ref.ref)

        # use pickle until a json format is supported
        model = pickle.loads(model_file)

        return model



    # save sklearn models in the provided format
    def save_to_ref(self, model: Any,
                          format: DataFormat,
                          base_ref: BaseRef,
                          options:Dict[str, Any] = None) -> None:

        blobstore_api: str = options["blob_api"] if options and "blob_api" in options else MODELSTORE_API


        blob:bytes = pickle.dumps(model)
        blob_id:str = self._create_blobstore_blob(blob, blobstore_api)

        #change base ref to point to blob id
        base_ref.ref = blob_id
        base_ref.refType = "modelstore"
