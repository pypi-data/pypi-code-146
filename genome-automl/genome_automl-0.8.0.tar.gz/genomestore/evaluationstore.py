from __future__ import print_function

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

from typing import Mapping, List, Tuple, Dict, Any

from .base import BaseRef, CodeRef, DataRef, Segment, ArtifactMeta, BaseMetric
from .card import CardArtifact
from .store import StoreContext, Store

from .materializers.factory import MaterializerRegistry, CardMaterializer, Materializer


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


EVALUATIONSTORE_API = os.getenv('GENOMESTORE')

class TaskSpec():

    def __init__(self,
      name: str = None,
      dataRef: DataRef = None,
      segment: Segment = None,
      prototypeRef: BaseRef = None,
      expectations: List[str] = None,
      context: dict = None):

        self.name = name
        self.dataRef = dataRef.__dict__ if dataRef else None
        self.segment = segment
        self.prototypeRef = prototypeRef.__dict__ if prototypeRef else None
        self.expectations = expectations
        self.context = context


    def get_meta(self):
        """
        :return: a dict with all the metadata fields of the task object
        """
        meta = {}

        # all props except weights blob and local file are metadata
        for k, v in self.__dict__.items():
            meta[k] = v


        return meta



class TaskArtifact(TaskSpec):

    def __init__(self,
      name: str = None,
      dataRef: DataRef = None,
      segment: str = None,
      prototypeRef: BaseRef = None,
      expectations: List[str] = None,
      context: dict = None,
      status:int = 0,
      metrics:dict = None,
      message:str = None):

        super().__init__(
          name = name,
          dataRef = dataRef,
          segment = segment,
          prototypeRef = prototypeRef,
          expectations = expectations,
          context = context)

        self.status = status
        self.metrics = metrics
        self.message = message




class ValidationSpec(ArtifactMeta):

    def __init__(self,
      canonicalName: str = None,
      application: str = None,
      target: str = None,
      versionName: str = None,
      specVersionName: str = None,
      code: CodeRef = None,
      parameters: dict = None,
      dataRefs: List[DataRef] = None,
      inputModality: str = None,
      framework: str = None,
      dimension: str = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target
        self.versionName = versionName
        self.specVersionName = versionName
        self.code = code.__dict__ if code else None
        self.parameters = parameters
        self.dataRefs = [ d.__dict__ for d in dataRefs ] if dataRefs else None

        self.inputModality = inputModality
        self.framework = framework
        self.dimension = dimension

        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation



class EvaluationSpec(ValidationSpec):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artifactType = "evaluationSpec"



    def createRun(self,
      pipelineName: str = None,
      pipelineStage: str = None,
      pipelineRunId: str = None,
      validationTarget: BaseRef = None,
      validationMetrics: List[BaseMetric] = None,
      tasks: List[TaskArtifact] = None,

      status: int = None,
      context: dict = None,

      user: str = None):

        return EvaluationArtifact(
          canonicalName = self.canonicalName,
          application = self.application,
          target = self.target,
          versionName = self.versionName,
          specVersionName = self.specVersionName,
          code = self.code,
          parameters = self.parameters,
          inputModality = self.inputModality,
          framework = self.framework,
          dimension = self.dimension,
          dataRefs = [DataRef(a["ref"], a["refType"]) for a in self.dataRefs] if self.dataRefs else None,

          pipelineName = pipelineName,
          pipelineStage = pipelineStage,
          pipelineRunId = pipelineRunId,
          validationTarget = validationTarget,
          validationMetrics = validationMetrics,
          tasks = tasks,

          status = status,
          context = context,

          user = user
        )





class TestSpec(EvaluationSpec):

    def __init__(self,
      canonicalName: str = None,
      application: str = None,
      target: str = None,
      versionName: str = None,
      specVersionName: str = None,
      code: CodeRef = None,
      parameters: dict = None,
      dataRefs: List[DataRef] = None,
      inputModality: str = None,
      framework: str = None,
      dimension: str = None):

        super().__init__(
          canonicalName = canonicalName,
          application = application,
          target = target,
          versionName = versionName,
          specVersionName = specVersionName,
          code = code,
          parameters = parameters,
          dataRefs = dataRefs,
          inputModality = inputModality,
          framework = framework,
          dimension = dimension)

        self.artifactType = "testSpec"





    def createRun(self,

      pipelineName: str = None,
      pipelineStage: str = None,
      pipelineRunId: str = None,
      validationTarget: BaseRef = None,
      validationMetrics: List[BaseMetric] = None,
      tasks: List[TaskArtifact] = None,

      status: int = None,
      context: dict = None,

      user: str = None):


        return TestArtifact(
          canonicalName = self.canonicalName,
          application = self.application,
          target = self.target,
          versionName = self.versionName,
          specVersionName = self.specVersionName,
          code = self.code,
          parameters = self.parameters,
          inputModality = self.inputModality,
          framework = self.framework,
          dimension = self.dimension,
          dataRefs = [DataRef(d["ref"], d["refType"]) for d in self.dataRefs] if self.dataRefs else None,

          pipelineName = pipelineName,
          pipelineStage = pipelineStage,
          pipelineRunId = pipelineRunId,
          validationTarget = validationTarget,
          validationMetrics = validationMetrics,
          tasks = tasks,

          status = status,
          context = context,

          user = user
        )




class EvaluationArtifact(EvaluationSpec):

    def __init__(self,
      canonicalName: str = None,
      application: str = None,
      target: str = None,
      versionName: str = None,
      specVersionName: str = None,
      code: CodeRef = None,
      parameters: dict = None,
      dataRefs: List[DataRef] = None,

      pipelineName: str = None,
      pipelineStage: str = None,
      pipelineRunId: str = None,
      validationTarget: BaseRef = None,
      validationMetrics: List[BaseMetric] = None,
      tasks: List[TaskArtifact] = None,

      inputModality: str = None,
      framework: str = None,
      dimension: str = None,
      status: int = None,
      context: dict = None,

      user: str = None):



        super().__init__(
          canonicalName = canonicalName,
          application = application,
          target = target,
          versionName = versionName,
          specVersionName = specVersionName,
          code = code,
          parameters = parameters,
          dataRefs = dataRefs)



        self.pipelineName = pipelineName
        self.pipelineStage = pipelineStage
        self.pipelineRunId = pipelineRunId

        self.validationTarget = validationTarget.__dict__ if validationTarget else None
        self.validationMetrics = [m.get_meta() for m in validationMetrics] if validationMetrics else []
        self.tasks = [task.get_meta() for task in tasks] if tasks else None

        self.inputModality = inputModality
        self.framework = framework
        self.dimension = dimension
        self.status = status
        self.context = context if context else None
        self.user = user if user else None

        self.artifactType = "evaluationArtifact"



    def add_metric(self, metric: BaseMetric):
        """
        :param metric: adds the provided metric object to overall list of metrics
        :return:
        """

        self.validationMetrics.append(metric.get_meta())


    def add_task(self, task: TaskArtifact):
        """
        :param task: adds the provided task run
        :return:
        """
        if self.tasks:
            self.tasks.append(task.get_meta())
        else:
            self.tasks = [task.get_meta()]



class TestArtifact(EvaluationArtifact):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)







class EvaluationStore(Store):

    def __init__(self, context: StoreContext):
        super().__init__(context)


    def _dict_to_artifact(self, artifact_meta: Dict[str, Any]) -> EvaluationSpec:

        artifactBlob = None
        if "artifactBlob" in artifact_meta and "ref" in artifact_meta["artifactBlob"]:
            artifactBlob = BaseRef(
              artifact_meta["artifactBlob"]["ref"],
              artifact_meta["artifactBlob"]["refType"])


        data_artifact_refs = None
        if "dataRefs" in artifact_meta and artifact_meta["dataRefs"]:
            data_artifact_refs = [DataRef(m["ref"], m["refType"]) for m in artifact_meta["dataRefs"]]

        epoch = datetime.datetime.utcfromtimestamp(0)

        artifactType = EvaluationArtifact
        if "artifactType" in artifact_meta:
            is_transform = artifact_meta["artifactType"] and artifact_meta["artifactType"].lower() == "evaluationSpec".lower()
            if is_transform:
                artifactType = TransformSpec


        artifact = artifactType(
          canonicalName = artifact_meta["canonicalName"],
          application = artifact_meta["application"],
          target = artifact_meta["target"] if "target" in artifact_meta else None,

          versionName = artifact_meta["versionName"],
          specVersionName = artifact_meta["specVersionName"],

          framework = artifact_meta["framework"] if "framework" in artifact_meta else None,
          inputModality = artifact_meta["inputModality"] if "inputModality" in artifact_meta else "tabular",
          code = self._get_artifact_code("code", artifact_meta),
          parameters = artifact_meta["parameters"] if "parameters" in artifact_meta else None,

          tags = artifact_meta["tags"] if "tags" in artifact_meta else None,
          context = artifact_meta["context"] if "context" in artifact_meta else None
        )

        if "id" in artifact_meta:
            artifact.id = artifact_meta["id"]


        if artifactType == EvaluationArtifact:

            artifact.validationMetrics = artifact_meta["validationMetrics"] if "validationMetrics" in artifact_meta else None
            artifact.status = artifact_meta["status"] if "status" in artifact_meta else None
            artifact.tasks = artifact_meta["tasks"] if "tasks" in artifact_meta else None


            artifact.pipelineName = artifact_meta["pipelineName"]
            artifact.pipelineStage = artifact_meta["pipelineStage"]
            artifact.pipelineRunId = artifact_meta["pipelineRunId"]

            artifact.validationTarget = artifact_meta["validationTarget"]
            artifact.dimension = artifact_meta["dimension"]


            artifact.artifactBlob = artifactBlob
            artifact.dataRefs = data_artifact_refs


            artifact.deployment = artifact_meta["deployment"]
            artifact.specDeployment = artifact_meta["specDeployment"]


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




        return artifact



    def _getEvaluationMeta(self, meta):

        # post model metadata
        evaluationMeta = {
            "canonicalName": meta["canonicalName"] if "canonicalName" in meta else "modelPipeline",
            "artifactType": meta["artifactType"] if "artifactType" in meta else "testArtifact",
            "application": meta["application"] if "application" in meta else "modelPipeline"
        }

        reqMeta = urllib.request.Request(EVALUATIONSTORE_API + "/v1.0/genome/search-validations")
        reqMeta.add_header(
            'Content-Type',
            'application/json',
        )

        responseMeta = urllib.request.urlopen(reqMeta, json.dumps(evaluationMeta).encode('utf-8'))
        data = responseMeta.read()
        evaluationMetaResp = json.loads(data)

        if not evaluationMetaResp or len(evaluationMetaResp) == 0:
            logging.info('No Test/Evaluation Found in EvaluationStore: ' + json.dumps(evaluationMeta))
            return None


        logging.info('Test/Evaluation Found in EvaluationStore: ' + json.dumps(evaluationMetaResp) + " len: " + str(len(evaluationMetaResp)))

        evaluationMetaArtifact = evaluationMetaResp[0]

        return evaluationMetaArtifact




    def load(self, meta):
        # first check with model store yada-yada
        evaluation = None
        evaluationMetaArtifact = None

        canonicalName = meta["canonicalName"]
        evaluationKey = meta["id"] if "id" in meta else None


        evaluationMetaArtifact = self._getEvaluationMeta(meta)

        return evaluationMetaArtifact




    def save(self, evaluation: EvaluationSpec) -> EvaluationSpec:
        return self.put_artifact(evaluation)

    def save_card(self, card: Any, card_artifact: CardArtifact, options:Dict[str, Any] = None):

        # get materializer by type
        materializer:CardMaterializer = self.get_materializer(type(card))

        # work on a copy meta artifact
        copy_artifact = pickle.loads(pickle.dumps(card_artifact))
        copy_artifact.artifactBlob = BaseRef("", "modelstore")



        # now save in blobstore and in metadata
        materializer.save(card, copy_artifact, options)

        logging.info("card artifact to save: ")
        logging.info(copy_artifact.to_json())
        return self.put_artifact(copy_artifact)



    def put_artifact(self, evaluation: EvaluationSpec) -> EvaluationSpec:

        # post evaluation metadata
        artifactType = "evaluationArtifact"
        if isinstance(evaluation, TestArtifact):
            artifactType = "testArtifact"
        elif isinstance(evaluation, EvaluationArtifact):
            artifactType = "evaluationArtifact"
        elif isinstance(evaluation, CardArtifact):
            artifactType = "cardArtifact"

        elif isinstance(evaluation, TestSpec):
            artifactType = "test"
        elif isinstance(evaluation, EvaluationSpec):
            artifactType = "evaluationSpec"




        reqMeta = urllib.request.Request(EVALUATIONSTORE_API + "/v1.0/genome/" + artifactType)
        reqMeta.add_header(
            'Content-Type',
            'application/json',
        )

        try:
            responseMeta = urllib.request.urlopen(reqMeta, evaluation.to_json().encode('utf-8'))
            data = responseMeta.read()
            modelMetaResp = json.loads(data)
            logging.info("model-id: " + str(modelMetaResp["id"]))
            evaluation.id = str(modelMetaResp["id"])
            return evaluation

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
