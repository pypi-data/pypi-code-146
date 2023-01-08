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


from ..estimator import GenomeEstimator



logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

try:
    import tensorflow as tf
except ImportError:
    warnings.warn('tensorflow could not be imported', ImportWarning)


MODELSTORE_API = os.getenv('BLOBSTORE') or os.getenv('GENOMESTORE')

GENOME_FILE = '_genome_.p'


class KerasModelMaterializer(ModelMaterializer):

    SUPPORTED_TYPES = (tf.keras.Model, tf.keras.Sequential, )


    def __init__(self):

        super().__init__()



    def load_ref(self, data_type: Type[Any],
                       format: DataFormat,
                       blob_refs: List[BaseRef],
                       options: Dict[str, Any] = None) -> Union[tf.keras.Model, tf.keras.Sequential, GenomeEstimator]:

        blobstore_api: str = options["blob_api"] if options and "blob_api" in options else MODELSTORE_API

        blob_ref = blob_refs[0] if len(blob_refs) else None


        # we are assuming we always load model files from the genome blob store
        response = urllib.request.urlopen(blobstore_api + "/v1.0/genome/blob/" + blob_ref.ref)
        model_file = response.read()



        logging.info("initializing tensorflow model from blob_ref:" + blob_ref.ref)

        tmpdir = tempfile.mkdtemp()
        z = zipfile.ZipFile(io.BytesIO(model_file))
        logging.info("files in zip:" + str(z.namelist()))
        z.extractall(tmpdir)
        tf_model = tf.keras.models.load_model(tmpdir)

        model = None
        if os.path.isfile(tmpdir + '/' + GENOME_FILE):
            model = pickle.load( open( tmpdir + '/' + GENOME_FILE, "rb" ))
            model.estimator = tf_model

        else:
            model = tf_model

        return model


    # save tensorflow models in the provided format
    def save_to_ref(self, model: Any,
                          format: DataFormat,
                          base_ref: BaseRef,
                          options:Dict[str, Any] = None) -> None:


        blobstore_api: str = options["blob_api"] if options and "blob_api" in options else MODELSTORE_API

        tmpdir = tempfile.mkdtemp()
        model_save_path = os.path.join(tmpdir, "model")
        os.makedirs(model_save_path, exist_ok=True)

        estimator = model

        if isinstance(model, GenomeEstimator):
            # remove estimator to not pickle the tensorflow model
            estimator = model.estimator
            model.estimator = None

            # save the genome meta file
            pickle.dump(model, open(model_save_path + '/' + GENOME_FILE, "wb"))


        tf.saved_model.save(estimator, model_save_path)

        shutil.make_archive(os.path.join(tmpdir, 'model-file'), 'zip', model_save_path)
        fileobj = open(tmpdir + "/model-file.zip", 'rb')
        blob:bytes = fileobj.read()
        fileobj.close()


        # store in blobstore
        blob_id:str = self._create_blobstore_blob(blob, blobstore_api)

        #change base ref to point to blob id
        base_ref.ref = blob_id
        base_ref.refType = "modelstore"
