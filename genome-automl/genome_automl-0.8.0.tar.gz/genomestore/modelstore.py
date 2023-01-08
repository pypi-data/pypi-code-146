from __future__ import print_function

import json
import logging
import sys
import time
import datetime
import os
import os.path
import pickle
import urllib.request
from urllib.error import  URLError


from typing import Mapping, List, Tuple, Dict, Type, Any


from .meta_extractor import ExtractorFactory

from .store import StoreContext, Store

from .base import BaseRef, CodeRef, DataRef, TransformSpec, TransformExecution, ModelArtifact
from .materializers.factory import MaterializerRegistry, ModelMaterializer, Materializer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


MODELSTORE_API = os.getenv('GENOMESTORE')
GENOME_FILE = '_genome_.p'
XGB_MODEL_FILE = 'xgb_model.json'


class ModelStore(Store):

    def __init__(self, context: StoreContext):
        super().__init__(context)
        self.cachedModels = {}

    def get_framework_materializer(self, framework_name: str) -> Materializer:
        return MaterializerRegistry.get_framework_materializer(framework_name)


    def _dict_to_transform_execution(self, execution_meta: Dict[str, Any]) -> TransformExecution:

        transform_execution = TransformExecution(
          execution_meta["execution_type"],
          execution_meta["instance_type"],
          execution_meta["provision_type"],
          count = execution_meta["count"],
          options = execution_meta["options"] if "options" in execution_meta else None
        )

        return transform_execution




    def _dict_to_artifact(self, artifact_meta: Dict[str, Any]) -> TransformSpec:

        artifactBlob = None
        if "artifactBlob" in artifact_meta and "ref" in artifact_meta["artifactBlob"]:
            artifactBlob = BaseRef(
              artifact_meta["artifactBlob"]["ref"],
              artifact_meta["artifactBlob"]["refType"])


        data_artifact_refs = None
        if "dataRefs" in artifact_meta and artifact_meta["dataRefs"]:
            data_artifact_refs = [DataRef(m["ref"], m["refType"]) for m in artifact_meta["dataRefs"]]

        epoch = datetime.datetime.utcfromtimestamp(0)

        artifactType = ModelArtifact
        if "artifactType" in artifact_meta:
            is_transform = artifact_meta["artifactType"] and artifact_meta["artifactType"].lower() == "transformSpec".lower()
            if is_transform:
                artifactType = TransformSpec


        artifact = artifactType(
          canonicalName = artifact_meta["canonicalName"],
          application = artifact_meta["application"],
          target = artifact_meta["target"] if "target" in artifact_meta else None,

          versionName = artifact_meta["versionName"],
          specVersionName = artifact_meta["specVersionName"],

          framework = artifact_meta["framework"] if "framework" in artifact_meta else None,
          frameworkOnlyInference = artifact_meta["frameworkOnlyInference"] if "frameworkOnlyInference" in artifact_meta else False,

          inputModality = artifact_meta["inputModality"] if "inputModality" in artifact_meta else "tabular",

          code = self._get_artifact_code("code", artifact_meta),
          inferenceCode = self._get_artifact_code("inferenceCode", artifact_meta),
          execution = self._dict_to_transform_execution(artifact_meta["execution"]) if "execution" in artifact_meta else None,

          parameters = artifact_meta["parameters"] if "parameters" in artifact_meta else None,

          tags = artifact_meta["tags"] if "tags" in artifact_meta else None,
          context = artifact_meta["context"] if "context" in artifact_meta else None
        )

        if "id" in artifact_meta:
            artifact.id = artifact_meta["id"]


        if artifactType == ModelArtifact:
            artifact.pipelineName = artifact_meta["pipelineName"]
            artifact.pipelineStage = artifact_meta["pipelineStage"]
            artifact.pipelineRunId = artifact_meta["pipelineRunId"]


            artifact.artifactBlob = artifactBlob
            artifact.dataRefs = data_artifact_refs

            artifact.deployment = artifact_meta["deployment"]
            artifact.specDeployment = artifact_meta["specDeployment"]

            artifact.checkpoint = artifact_meta["checkpoint"] if "checkpoint" in artifact_meta else None
            artifact.epoch = artifact_meta["epoch"] if "epoch" in artifact_meta else None


            if ("artifactStartTime" in artifact_meta and
              artifact_meta["artifactStartTime"] and
              isinstance(artifact_meta["artifactStartTime"], (int, float))):
                artifact.artifactStartTime = (epoch + datetime.timedelta(
                  milliseconds = artifact_meta["artifactStartTime"]))

            if ("artifactTime" in artifact_meta and
              artifact_meta["artifactTime"] and
              isinstance(artifact_meta["artifactTime"], (int, float))):
                artifact.artifactTime = (epoch + datetime.timedelta(
                  milliseconds = artifact_meta["artifactTime"]))


            artifact.metrics = artifact_meta["metrics"] if "metrics" in artifact_meta else None


        return artifact



    def _get_model_meta(self, meta: Dict[str, Any]) -> Dict[str, Any]:

        # post model metadata
        modelMeta = {
            "canonicalName": meta["canonicalName"] if "canonicalName" in meta else "modelPipeline",
            "application": meta["application"] if "application" in meta else "modelPipeline",
            "target": meta["target"] if "target" in meta else "modelTarget"
        }

        reqMeta = urllib.request.Request(MODELSTORE_API + "/v1.0/genome/search")
        reqMeta.add_header(
            'Content-Type',
            'application/json',
        )

        responseMeta = urllib.request.urlopen(reqMeta, json.dumps(modelMeta).encode('utf-8'))
        data = responseMeta.read()
        modelMetaResp = json.loads(data)

        if not modelMetaResp or len(modelMetaResp) == 0:
            logging.info('No Model Found in ModelStore: ' + json.dumps(modelMeta))
            return None


        logging.info('Models Found in ModelStore: ' + json.dumps(modelMetaResp) + " len: " + str(len(modelMetaResp)))

        modelMetaArtifact =  modelMetaResp[0]

        return modelMetaArtifact




    def _load_model_artifact(self, model_id: str, model_artifact: ModelArtifact, explainer:bool = False) -> Any:

        model = None

        cacheSuffix: str = ""
        if explainer:
            cacheSuffix = "explainer"

        # get materializer by framework
        framework_name: str = model_artifact.framework.split(":")[0]

        materializer: ModelMaterializer = self.get_framework_materializer(framework_name)
        supported_type: Type[Any] = materializer.SUPPORTED_TYPES[0]

        # load model
        loaded_model: Any = materializer.load(supported_type, [model_artifact])


        # cache model and metadata
        self.cachedModels[model_id] = loaded_model
        self.cachedModels[model_artifact.canonicalName + cacheSuffix] = loaded_model
        self.cachedModels[model_artifact.id + cacheSuffix] = loaded_model
        self.cachedModels["/meta/" + model_artifact.canonicalName] = model_artifact
        self.cachedModels["/meta/" + model_artifact.id] = model_artifact



        return loaded_model




    def load_model(self, meta, withMeta=False, explainer=False):
        return self.load(meta, withMeta=withMeta)

    def load_explainer(self, meta, withMeta=False):
        return self.load(meta, withMeta=withMeta, explainer=True)

    def load(self, meta, withMeta=False, explainer=False):
        # first check with model store yada-yada
        model = None
        modelMetaArtifact = None

        canonicalName = meta["canonicalName"]
        modelKey = meta["id"] if "id" in meta else None

        cacheKey = modelKey if modelKey else canonicalName
        cacheSuffix = ""
        metaCacheKey = "/meta/" + cacheKey

        blobRefName = "ref"
        if explainer:
            blobRefName = "explainerRef"
            cacheSuffix = "explainer"
            cacheKey = cacheKey + cacheSuffix


        # retrieve from cache if exists
        if metaCacheKey in self.cachedModels and self.cachedModels[metaCacheKey]:
            logging.info("using cached model for: " + metaCacheKey)

            # this retrieves a ModelArtifact type object not a dict
            modelMetaArtifact = self.cachedModels[metaCacheKey]

            if modelMetaArtifact.id + cacheSuffix in self.cachedModels:
                if withMeta:
                    return self.cachedModels[modelMetaArtifact.id + cacheSuffix], modelMetaArtifact

                return self.cachedModels[modelMetaArtifact.id + cacheSuffix]




        if "framework" not in meta or "artifactBlob" not in meta:
            if not modelMetaArtifact:
                modelMetaArtifact = self._get_model_meta(meta)

            if not modelMetaArtifact:
                if withMeta:
                    return None, None
                return None

            if blobRefName in modelMetaArtifact["artifactBlob"]:
                model_id = modelMetaArtifact["artifactBlob"][blobRefName]
                logging.info('Model Found in ModelStore: ' + json.dumps(modelMetaArtifact["artifactBlob"]))


        else:
            modelMetaArtifact = meta
            if blobRefName in modelMetaArtifact["artifactBlob"]:
                model_id = modelMetaArtifact["artifactBlob"][blobRefName]




        if model_id:
            #TODO change type to ModelArtifact
            logging.info("fetching model from url: " + MODELSTORE_API + "/v1.0/genome/blob/" + model_id)
            model_artifact = self._dict_to_artifact(modelMetaArtifact)
            model = self._load_model_artifact(model_id, model_artifact, explainer=explainer)


        if withMeta:
            return (model, modelMetaArtifact)


        return model





    def save(self, model: Any, model_artifact: ModelArtifact, options: Dict[str, Any] = None) -> ModelArtifact:

        # get materializer by type,
        # use estimator type for genomeestimator models
        model_type: Type[Any] = type(model)
        if hasattr(model, "estimator"):
            model_type = type(model.estimator)

        materializer:ModelMaterializer = self.get_materializer(model_type)

        # work on a copy meta artifact
        copy_artifact = pickle.loads(pickle.dumps(model_artifact))
        copy_artifact.artifactBlob = BaseRef("", "modelstore")

        # extract parameters
        extractor: ModelMetaExtractor = ExtractorFactory.get_parameter_extractor(model_type)
        extractedParams: dict = extractor.extract(model.estimator if hasattr(model, "estimator") else model)

        # save in blobstore
        materializer.save(model, copy_artifact, options)


        if extractedParams and not copy_artifact.parameters:
            copy_artifact.parameters = {}

        if extractedParams:
            for key, val in extractedParams.items():
              copy_artifact.parameters[key] = val


        return self.put_artifact(copy_artifact)




    def put_artifact(self, model_artifact: ModelArtifact) -> ModelArtifact:

        # post model metadata
        reqMeta = urllib.request.Request(MODELSTORE_API + "/v1.0/genome/modelArtifact")
        reqMeta.add_header(
            'Content-Type',
            'application/json',
        )


        try:

            logging.info(f'Saving model artifact in ModelStore: {MODELSTORE_API}')

            response_meta = urllib.request.urlopen(reqMeta, model_artifact.to_json().encode('utf-8'))
            data = response_meta.read()
            model_meta_json = json.loads(data)


            logging.info("model-id: " + str(model_meta_json["id"]))
            copy_artifact = pickle.loads(pickle.dumps(model_artifact))
            copy_artifact.id = str(model_meta_json["id"])

            return copy_artifact


        except URLError as e:
            if hasattr(e, 'reason'):
                logging.info('We failed to reach a server.')
                logging.info('Reason: ' + e.reason)

            if hasattr(e, 'code'):
                logging.info('The server couldn\'t fulfill the request.')
                logging.info('Error code: ' + str(e.code))

            if hasattr(e, 'msg'):
                logging.info('The server couldn\'t fulfill the request.')
                logging.info('Error message: ' + str(e.msg))


            # still throw it
            raise e
