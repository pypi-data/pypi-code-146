
from typing import Mapping, List, Tuple, Dict, Any

import json
import logging
import datetime

from .pipelines.expression_evaluators.expression_evaluator import Expression


class BaseRef():
    def __init__(self, ref:str, refType:str):
        self.ref = ref
        self.refType = refType

    def __eq__(self, other) -> bool:
        return (self.refType, self.ref) == (other.refType, other.ref)


"""
Data related base objects, Datasets and Segments
"""
class DataRef(BaseRef):
    def __init__(self, ref:str, refType:str):
        super().__init__(ref, refType)

class DataArtifactRef(DataRef):
    def __init__(self, ref:str):
        super().__init__(ref, "dataArtifact-id")

class DatasetRef(DataRef):
    def __init__(self, ref:str):
        super().__init__(ref, "dataset-id")


class SegmentFilter():
    def __init__(self, recipeType:str, recipe:str):
        self.recipeType = recipeType
        self.recipe = recipe


class Segment():
    def __init__(self, name:str, filters:List[SegmentFilter]):
        self.name = name
        self.filters = filters



class ArtifactMeta():



    def get_meta(self) -> Dict[Any, Any]:
        """
        :return: a dict with all the metadata fields of the artifact object
        """
        meta = {}

        # all props except those starting with underscore are metadata
        for k, v in self.__dict__.items():
            if isinstance(v, BaseRef):
                meta[k] = v.__dict__
            elif isinstance(v, List):
                meta[k] = [ref.__dict__ if isinstance(ref, BaseRef) else ref for ref in v]
            elif isinstance(v, TransformExecution):
                meta[k] = v.__dict__
            elif isinstance(v, datetime.datetime):
                # convert to utc tz and get millis since epoch
                v_utc:datetime.datetime = v.astimezone(datetime.timezone.utc)
                meta[k] = round(v_utc.timestamp() * 1000)

            elif isinstance(v, Expression):
                meta[k] = v.get_meta()

            elif isinstance(v, dict):
                meta[k] = self._get_dict_meta(v)

            elif v == None: # skip properties that are not set
                pass
            else:
                meta[k] = v


        return meta


    # converts expressions embedded in params etc.
    def _get_dict_meta(self, o):
        meta = {}
        
        for k, v in o.items():
            if isinstance(v, (int, float, bool, str)):
                meta[k] = v
            elif isinstance(v, list):
                meta[k] = [self._get_dict_meta(e) if isinstance(e, dict) else e for e in v]
            elif isinstance(v, dict):
                meta[k] = self._get_dict_meta(v)
            elif isinstance(v, Expression):
                meta[k] = v.get_meta()
            else:
                meta[k] = v

        return meta



    def to_json(self) -> str:
        return json.dumps(self.get_meta())



class Dataset(ArtifactMeta):

    def __init__(self,
      canonicalName: str = None,
      application: str = None,
      target: str = None,
      format: str = None, # [json, csv, parquet, avro, ]
      versionName: str = None,
      schema: dict = None,
      inputDatasets: List[DataRef] = None,
      context: dict = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target

        self.format = format
        self.versionName = versionName
        self.schema = schema
        self.dataRefs = inputDatasets
        self.context = context

        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation


class DataSpec(ArtifactMeta):

    def __init__(self,

      canonicalName: str = None,
      application: str = None,
      target: str = None,
      versionName: str = None,
      specVersionName: str = None,
      datasetId: str = None,
      artifactKind: str = "batch", # batch | record

      context: dict = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target

        self.format = format
        self.versionName = versionName
        self.specVersionName = specVersionName
        self.datasetId = datasetId

        self.artifactKind = artifactKind

        self.artifactType = "dataSpec"

        self.context = context


class DataArtifact(DataSpec):

    def __init__(self,

      canonicalName: str = None,
      application: str = None,
      target: str = None,
      pipelineName: str = None,
      pipelineRunId: str = None,
      pipelineStage: str = None,
      format: str = None, # [json, csv, parquet, avro, ]
      versionName: str = None,
      specVersionName: str = None,
      datasetId: str = None,
      artifactKind: str = "batch", # batch | record

      inputDataArtifacts: List[DataRef] = None, # input artifacts that produced this data artifact

      artifactRef: DataRef = None, # pointer to raw files in storage

      startTime: datetime.datetime = None, #lower time bound of the data contained in this artifact
      endTime: datetime.datetime = None, #upper time bound of the data contained in this artifact

      context: dict = None,
      metrics: dict = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target
        self.pipelineName = pipelineName
        self.pipelineRunId = pipelineRunId
        self.pipelineStage = pipelineStage
        self.format = format
        self.versionName = versionName
        self.specVersionName = specVersionName
        self.datasetId = datasetId

        self.artifactKind = artifactKind
        self.dataRefs = inputDataArtifacts

        self.artifactRef = artifactRef

        self.artifactStartTime = startTime
        self.artifactTime = endTime

        self.context = context
        self.metrics = metrics

        self.artifactType = "dataArtifact"

        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation





"""
Metrics related base objects, NumericMetric, DistributionMetric, ...
"""


class BaseMetric():
    def __init__(self, name:str, value:Any):
        self.name = name
        self.value = value


    def get_meta(self) -> Dict[Any, Any]:
        """
        :return: a dict with the fields of the metric object
        """
        meta = {}

        # all props are metadata
        for k, v in self.__dict__.items():
            meta[k] = v


        return meta



class NumericMetric(BaseMetric):
    def __init__(self, name:str, value:float):
        super().__init__(name, value)



"""
Transformation related base objects, CodeRef
"""

class CodeRef(BaseRef):
    def __init__(self, ref:str, refType:str, version:str = "1.0.0"):
        super().__init__(ref, refType)
        self.version = version

class TransformExecution():
    def __init__(self, instance_type:str, provision_type: str, execution_type:str = "batch", count:int = 1, options:Dict[Any, Any] = None):
        self.execution_type = execution_type  # [Batch, Sagemaker, EMR, ...]
        self.instance_type = instance_type  # e2-highcpu-2 etc.
        self.provision_type = provision_type  # SPOT, STANDARD
        self.count = count
        self.options = options # will be sent to execution engine as is



class TransformSpec(ArtifactMeta):
    def __init__(self,

      canonicalName: str = None,
      application: str = None,
      target: str = None,

      code: CodeRef = None,
      inferenceCode: CodeRef = None,

      execution: TransformExecution = None,


      parameters: dict = None,

      framework: str = None, # [tensorflow, keras, sklearn, xgboost, pyspark]
      frameworkOnlyInference: bool = False, # only the framework version is required to predict, no other code
      inputModality: str = None, # image | text | tabular | mixed

      versionName: str = None, # version name of the whole config for this model
      specVersionName: str = None, # version name of the code/template for this model

      tags: dict = None,
      context: dict = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target
        self.code = code
        self.inferenceCode = inferenceCode
        self.execution = execution
        self.parameters = parameters

        self.framework = framework
        self.frameworkOnlyInference = frameworkOnlyInference
        self.inputModality = inputModality

        self.versionName = versionName
        self.specVersionName = specVersionName


        self.tags = tags
        self.context = context

        self.artifactType = "transformSpec"



class ModelArtifact(TransformSpec):

    def __init__(self,

      canonicalName: str = None,
      application: str = None,
      target: str = None,

      code: CodeRef = None,
      inferenceCode: CodeRef = None,
      execution: TransformExecution = None,

      parameters: dict = None,

      pipelineName: str = None,
      pipelineRunId: str = None,
      pipelineStage: str = None,

      framework: str = None, # [tensorflow, keras, sklearn, xgboost, pyspark]
      frameworkOnlyInference: bool = True, # only the framework version is required to predict, no other code
      inputModality: str = None, # image | text | tabular | mixed

      versionName: str = None, # version name of the whole config for this model
      specVersionName: str = None, # version name of the code/template for this model

      deployment: str = None, # whole config/spec deployment, which changes even if template is same
      specDeployment: str = None, # template config/spec deployment

      inputDataArtifacts: List[DataRef] = None, # input artifacts that produced this artifact

      artifactBlob: BaseRef = None, # pointer to raw files in storage

      checkpoint: str = None, # checkpoint name
      epoch: int = None,

      startTime: datetime.datetime = None, #lower time bound of the data contained in this artifact
      endTime: datetime.datetime = None, #upper time bound of the data contained in this artifact

      tags: dict = None,
      context: dict = None,
      metrics: dict = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target
        self.code = code
        self.inferenceCode = inferenceCode
        self.execution = execution

        self.parameters = parameters

        self.pipelineName = pipelineName
        self.pipelineRunId = pipelineRunId
        self.pipelineStage = pipelineStage

        self.framework = framework
        self.frameworkOnlyInference = frameworkOnlyInference
        self.inputModality = inputModality

        self.versionName = versionName
        self.specVersionName = specVersionName

        self.deployment = deployment
        self.specDeployment = specDeployment

        self.dataRefs = inputDataArtifacts

        self.artifactBlob = artifactBlob

        self.checkpoint = checkpoint
        self.epoch = epoch

        self.artifactStartTime = startTime
        self.artifactTime = endTime

        self.tags = tags
        self.context = context
        self.metrics = metrics

        self.artifactType = "modelArtifact"

        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation
