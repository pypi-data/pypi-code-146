from __future__ import annotations

import functools
import logging
import json
import os

from .flow_parser import FlowGraph

from typing import Mapping, List, Tuple, Dict, Any

from ..base import ArtifactMeta, DataSpec, TransformSpec, DataArtifact, ModelArtifact
from ..card import CardArtifact
from ..evaluationstore import EvaluationSpec, EvaluationArtifact

from ..store import StoreContext, Store

from ..datastore import DataStore
from ..modelstore import ModelStore
from ..evaluationstore import EvaluationStore

import sys



class StepInput():

    def get_meta(self) -> Dict[str, Any]:

        meta = {
          "cls_name": self._cls_name
        }

        if getattr(self, "data_specs", None):
            if self.data_specs:
                meta["data_specs"] = [m.get_meta() for m in self.data_specs]

        if getattr(self, "data_artifacts", None):
            if self.data_artifacts:
                meta["data_artifacts"] = [m.get_meta() for m in self.data_artifacts]

        if getattr(self, "transform_spec", None):
            if self.transform_spec:
                meta["transform_spec"] = self.transform_spec.get_meta()

        if getattr(self, "model_artifacts", None):
            if self.model_artifacts:
                meta["model_artifacts"] = [m.get_meta() for m in self.model_artifacts]


        if getattr(self, "evaluation_specs", None):
            if self.evaluation_specs:
                meta["evaluation_specs"] = [m.get_meta() for m in self.evaluation_specs]

        if getattr(self, "evaluation_artifacts", None):
            if self.evaluation_artifacts:
                meta["evaluation_artifacts"] = [m.get_meta() for m in self.evaluation_artifacts]


        # push step input properties
        if getattr(self, "model_artifact", None):
            if self.model_artifact:
                meta["model_artifact"] = self.model_artifact.get_meta()

        if getattr(self, "data_artifact", None):
            if self.model_artifact:
                meta["data_artifact"] = self.data_artifact.get_meta()

        if getattr(self, "evaluation_artifact", None):
            if self.evaluation_artifact:
                meta["evaluation_artifact"] = self.evaluation_artifact.get_meta()

        if getattr(self, "card_artifact", None):
            if self.card_artifact:
                meta["card_artifact"] = self.card_artifact.get_meta()


        # pipeline deploy step input properties
        if getattr(self, "pipeline_meta", None):
            if self.pipeline_meta:
                meta["pipeline_meta"] = self.pipeline_meta


        # query step input properties
        if getattr(self, "query_spec", None):
            if self.query_spec:
                meta["query_spec"] = self.query_spec

        # query step output properties
        if getattr(self, "query_results", None):
            if self.query_results:
                meta["query_results"] = [m.get_meta() for m in self.query_results]




        return meta



    @staticmethod
    def from_meta(meta: Dict[str, Any]) -> StepInput:

        data_store = DataStore(StoreContext())
        model_store = ModelStore(StoreContext())
        evaluation_store = EvaluationStore(StoreContext())

        entity_type_name = meta["cls_name"]

        artifact_types = {
          "TransformInput": TransformInput,
          "TransformOutput": TransformOutput,
          "DataTransformInput": DataTransformInput,
          "DataTransformOutput": DataTransformOutput,
          "PushModelInput": PushModelInput,
          "PushDataArtifactInput": PushDataArtifactInput,
          "PushEvaluationInput": PushEvaluationInput,
          "PushCardInput": PushCardInput,
          "PushPipelineInput": PushPipelineInput,
          "QueryInput": QueryInput,
          "QueryOutput": QueryOutput,
        }

        entity_type = artifact_types[entity_type_name]

        if entity_type in [TransformInput, DataTransformInput]:
            data_specs = [data_store._dict_to_artifact(m) for m in meta["data_specs"]] if "data_specs" in meta else None
            transform_spec = model_store._dict_to_artifact(meta["transform_spec"])
            evaluation_specs = [evaluation_store._dict_to_artifact(m) for m in meta["evaluation_specs"]] if "evaluation_specs" in meta else None


            return entity_type(data_specs, transform_spec, evaluation_specs)

        if entity_type == TransformOutput:
            model_artifacts = [model_store._dict_to_artifact(m) for m in meta["model_artifacts"]]
            evaluation_artifacts = [evaluation_store._dict_to_artifact(m) for m in meta["evaluation_artifacts"]] if "evaluation_artifacts" in meta else None

            return entity_type(model_artifacts, evaluation_artifacts)

        if entity_type == DataTransformOutput:
            data_artifacts = [data_store._dict_to_artifact(m) for m in meta["data_artifacts"]]
            evaluation_artifacts = [evaluation_store._dict_to_artifact(m) for m in meta["evaluation_artifacts"]] if "evaluation_artifacts" in meta else None

            return entity_type(data_artifacts, evaluation_artifacts)


        if entity_type == PushModelInput:
            return entity_type(model_store._dict_to_artifact(meta["model_artifact"]))


        if entity_type == PushDataArtifactInput:
            return entity_type(data_store._dict_to_artifact(meta["data_artifact"]))


        if entity_type == PushEvaluationInput:
            return entity_type(evaluation_store._dict_to_artifact(meta["evaluation_artifact"]))


        if entity_type == PushCardInput:
            return entity_type(evaluation_store._dict_to_artifact(meta["card_artifact"]))

        if entity_type == PushPipelineInput:
            return entity_type(meta["pipeline_meta"])


        if entity_type == QueryInput:
            return entity_type(meta["query_spec"])


        if entity_type == QueryOutput:
            # generate artifact objects contained in query results from respective dicts
            artifact_list = [StepInput.from_artifact_meta(m, data_store, model_store, evaluation_store)
                for m in meta["query_results"]
            ] if meta["query_results"] else []

            return entity_type(artifact_list)



    @staticmethod
    def from_artifact_meta(meta: Dict[str, Any], data_store:DataStore,
       model_store:ModelStore,
       evaluation_store:EvaluationStore) -> ArtifactMeta:

        # if no artifactType key is found we should error out
        artifact_type = meta["artifactType"]

        if artifact_type in ["evaluationArtifact", "evaluationSpec", "testArtifact"]:
            return evaluation_store._dict_to_artifact(meta)

        elif artifact_type in ["modelArtifact", "transformSpec"]:
            return model_store._dict_to_artifact(meta)

        elif artifact_type in ["dataArtifact", "dataSpec", "dataset"]:
            return data_store._dict_to_artifact(meta)



class TransformInput(StepInput):
    def __init__(self, data_specs: List[DataSpec], transform_spec: TransformSpec, evaluation_specs: List[EvaluationSpec]):
        self.data_specs = data_specs
        self.transform_spec = transform_spec
        self.evaluation_specs = evaluation_specs
        self._cls_name = "TransformInput"


class TransformOutput(StepInput):
    def __init__(self, model_artifacts: List[ModelArtifact], evaluation_artifacts: List[EvaluationArtifact]):

        self.model_artifacts = model_artifacts
        self.evaluation_artifacts = evaluation_artifacts
        self._cls_name = "TransformOutput"



class DataTransformInput(StepInput):
    def __init__(self, data_specs: List[DataSpec], transform_spec: TransformSpec, evaluation_specs: List[EvaluationSpec]):
        self.data_specs = data_specs
        self.transform_spec = transform_spec
        self.evaluation_specs = evaluation_specs
        self._cls_name = "DataTransformInput"


class DataTransformOutput(StepInput):
    def __init__(self, data_artifacts: List[DataArtifact], evaluation_artifacts: List[EvaluationArtifact]):
        self.data_artifacts = data_artifacts
        self.evaluation_artifacts = evaluation_artifacts
        self._cls_name = "DataTransformOutput"




class PushModelInput(StepInput):
    def __init__(self, model_artifact: ModelArtifact):
        self.model_artifact = model_artifact
        self._cls_name = "PushModelInput"


class PushDataArtifactInput(StepInput):
    def __init__(self, data_artifact: DataArtifact):
        self.data_artifact = data_artifact
        self._cls_name = "PushDataArtifactInput"


class PushEvaluationInput(StepInput):
    def __init__(self, evaluation_artifact: EvaluationArtifact):
        self.evaluation_artifact = evaluation_artifact
        self._cls_name = "PushEvaluationInput"

class PushCardInput(StepInput):
    def __init__(self, card_artifact: CardArtifact):
        self.card_artifact = card_artifact
        self._cls_name = "PushCardInput"


class PushPipelineInput(StepInput):
    def __init__(self, pipeline_meta: Dict):
        self.pipeline_meta = pipeline_meta
        self._cls_name = "PushPipelineInput"



class QueryInput(StepInput):
    def __init__(self, query_spec: Dict):
        self.query_spec = query_spec
        self._cls_name = "QueryInput"


class QueryOutput(StepInput):
    def __init__(self, query_results: List[ArtifactMeta]):
        self.query_results = query_results
        self._cls_name = "QueryOutput"
