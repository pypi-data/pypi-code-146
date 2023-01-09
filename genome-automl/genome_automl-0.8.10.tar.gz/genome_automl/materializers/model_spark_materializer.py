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
    from pyspark.ml import PipelineModel
    from pyspark.ml.tree import _TreeEnsembleModel
    from pyspark.sql import SparkSession, SQLContext

    spark = SparkSession.builder.master("local[*]").appName("DTree-Classification-California-Housing").getOrCreate()
    spark_reader = PipelineModel.read().session(spark)

except ImportError:
    warnings.warn('pyspark PipelineModel cannot be imported', ImportWarning)



MODELSTORE_API = os.getenv('BLOBSTORE') or os.getenv('GENOMESTORE')

GENOME_FILE = '_genome_.p'


class SparkModelMaterializer(ModelMaterializer):

    SUPPORTED_TYPES = (PipelineModel, _TreeEnsembleModel, )


    def __init__(self):

        super().__init__()



    def load_ref(self, data_type: Type[Any],
                       format: DataFormat,
                       blob_refs: List[BaseRef],
                       options: Dict[str, Any] = None) -> Union[PipelineModel, GenomeEstimator]:


        blobstore_api: str = options["blob_api"] if options and "blob_api" in options else MODELSTORE_API

        blob_ref = blob_refs[0] if len(blob_refs) else None


        # we are assuming we always load model files from the genome blob store
        response = urllib.request.urlopen(blobstore_api + "/v1.0/genome/blob/" + blob_ref.ref)
        model_file = response.read()


        # load into local dir and initialize Spark model
        logging.info("initializing Spark model from blob_ref:" + blob_ref.ref)
        start_milli = int(round(time.time() * 1000))
        logging.info("started loading spark model:" + str(start_milli))

        tmpdir = tempfile.mkdtemp()
        z = zipfile.ZipFile(io.BytesIO(model_file))
        logging.info("files in zip:" + str(z.namelist()))
        z.extractall(tmpdir)

        start_milli = int(round(time.time() * 1000))
        logging.info("started using load() model:" + str(start_milli))

        pipeline_model = spark_reader.load(tmpdir)

        logging.info("finished loading spark pipeline from model store:" + str(int(round(time.time() * 1000)) - start_milli) )


        if len(pipeline_model.stages) == 1:
            pipeline_model = pipeline_model.stages[-1]

        model = None
        if os.path.isfile(tmpdir + '/' + GENOME_FILE):
            model = pickle.load(open( tmpdir + '/' + GENOME_FILE, "rb" ))
            model.estimator = pipeline_model
        else:
            model = pipeline_model

        logging.info("finished loading genome model from file:" + str(int(round(time.time() * 1000)) - start_milli) )


        return model


    # save spark models in the provided format
    def save_to_ref(self, model: Any,
                          format: DataFormat,
                          base_ref: BaseRef,
                          options:Dict[str, Any] = None) -> None:

        blobstore_api: str = options["blob_api"] if options and "blob_api" in options else MODELSTORE_API

        tmpdir = tempfile.mkdtemp()
        model_save_path = os.path.join(tmpdir, "model")

        estimator = model

        if isinstance(model, GenomeEstimator):
            # remove estimator to not pickle the spark model
            estimator = model.estimator
            model.estimator = None



        if not "pipeline" in str(type(estimator)).lower():
          pipe_model = PipelineModel([estimator])
          pipe_model.save(model_save_path)
        else:
          estimator.save(model_save_path)

        # exist ok true
        os.makedirs(model_save_path, exist_ok=True)

        if isinstance(model, GenomeEstimator):
            # save the genome meta file
            pickle.dump(model, open(model_save_path + '/' + GENOME_FILE, "wb"))




        shutil.make_archive(os.path.join(tmpdir, 'model-file'), 'zip', model_save_path)
        fileobj = open(tmpdir + "/model-file.zip", 'rb')
        blob:bytes = fileobj.read()
        fileobj.close()


        # store in blobstore
        blob_id:str = self._create_blobstore_blob(blob, blobstore_api)

        #change base ref to point to blob id
        base_ref.ref = blob_id
        base_ref.refType = "modelstore"
