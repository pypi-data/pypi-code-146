from __future__ import print_function

import json
import logging
import sys
import time
import datetime
import os
import os.path
import pickle
import urllib.parse
import urllib.request
from urllib.error import  URLError
import base64
import io
import glob
import tempfile
import zipfile
import shutil
import uuid
import hashlib


import warnings
from typing import Mapping, List, Tuple, Dict, Union, Type, Any


from .base import BaseRef, CodeRef, DataRef, Segment, ArtifactMeta, DataSpec, Dataset, DataArtifact, BaseMetric
from .materializers.factory import MaterializerRegistry, DataFrameMaterializer
from .store import StoreContext, Store

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


DATASTORE_API = os.getenv('GENOMESTORE')


class DataStore(Store):

    def __init__(self, context: StoreContext):

        super().__init__(context)


    # method to query for data artifact or dataset metadata
    def _get_dataset_meta(self, meta: Dict[str, Any],
        from_time: datetime.datetime = None,
        to_time: datetime.datetime = None, limit: int = None) -> Union[Dict, List]:

        #  query data properties
        data_query = {
            "canonicalName": meta["canonicalName"] if "canonicalName" in meta else "modelPipeline",
            "artifactType": meta["artifactType"] if "artifactType" in meta else "dataset",
            "application": meta["application"] if "application" in meta else "modelPipeline"
        }

        if "id" in meta:
            data_query["id"] = meta["id"]


        if "datasetId" in meta:
            data_query["datasetId"] = meta["datasetId"]


        if "pipelineName" in meta:
            data_query["pipelineName"] = meta["pipelineName"]


        if "pipelineStage" in meta:
            data_query["pipelineStage"] = meta["pipelineStage"]


        req_params = {}
        if from_time:
            req_params["from"] = str(round(from_time.timestamp() * 1000))

        if to_time:
            req_params["to"] = str(round(to_time.timestamp() * 1000))

        if limit:
            req_params["limit"] = str(limit)

        query_string = urllib.parse.urlencode( req_params )
        query_string = ("?" + query_string) if query_string else ""

        reqMeta = urllib.request.Request(DATASTORE_API + "/v1.0/genome/search-data" + query_string)
        reqMeta.add_header(
            'Content-Type',
            'application/json',
        )

        responseMeta = urllib.request.urlopen(reqMeta, json.dumps(data_query).encode('utf-8'))
        data = responseMeta.read()
        dataset_meta_resp = json.loads(data)

        if not dataset_meta_resp or len(dataset_meta_resp) == 0:
            logging.info('No dataset or dataArtifacts found in DataStore: ' + json.dumps(data_query))
            return None


        logging.info('dataset found in DataStore: ' + json.dumps(dataset_meta_resp) + " len: " + str(len(dataset_meta_resp)))


        datasetArtifacts = None

        if data_query["artifactType"] == "dataset" :

            datasetArtifacts = dataset_meta_resp[0]
        else:

            datasetArtifacts = dataset_meta_resp


        return datasetArtifacts


    def _dict_to_artifact(self, artifact_meta: Dict[str, Any]) -> DataSpec:

        artifactBlob = None
        if "artifactRef" in artifact_meta and "ref" in artifact_meta["artifactRef"]:
            artifactBlob = DataRef(artifact_meta["artifactRef"]["ref"], artifact_meta["artifactRef"]["refType"])


        data_artifact_refs = None
        if "dataRefs" in artifact_meta and artifact_meta["dataRefs"]:
            data_artifact_refs = [DataRef(m["ref"], m["refType"]) for m in artifact_meta["dataRefs"]]

        epoch = datetime.datetime.utcfromtimestamp(0)

        artifactType = DataArtifact
        if "artifactType" in artifact_meta:
            is_data_spec = artifact_meta["artifactType"] and artifact_meta["artifactType"].lower() == "dataSpec".lower()
            if is_data_spec:
                artifactType = DataSpec

        artifact = artifactType(
          canonicalName = artifact_meta["canonicalName"],
          application = artifact_meta["application"],

          target = artifact_meta["target"]if "target" in artifact_meta else None,

          versionName = artifact_meta["versionName"],
          specVersionName = artifact_meta["specVersionName"],

          format = artifact_meta["format"],

          datasetid = artifact_meta["dataset"],
          artifactKind = artifact_meta["artifactKind"] if "artifactKind" in artifact_meta else "batch",

          context = artifact_meta["context"] if "context" in artifact_meta else None,
        )

        if "id" in artifact_meta:
            artifact.id = artifact_meta["id"]

        if artifactType == DataArtifact:

            artifact.pipelineName = artifact_meta["pipelineName"]
            artifact.pipelineStage = artifact_meta["pipelineStage"]
            artifact.pipelineRunId = artifact_meta["pipelineRunId"]

            artifact.dataRefs = data_artifact_refs
            artifact.artifactRef = artifactBlob

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


    # methods to get datasets or data artifacts

    def get_dataset(self, meta: Dict[str, Any]) -> Dataset:

        meta["artifactType"] = "dataset"

        datasetEntry: Dict[str, Any] = self._get_dataset_meta(meta)
        inputDatasets:List[DataRef] = [
          DataRef(data_ref["ref"], data_ref["refType"]) for data_ref in datasetEntry["dataRefs"]
        ] if "dataRefs" in  datasetEntry and datasetEntry["dataRefs"] else None

        if datasetEntry:
            dataset = Dataset(
              canonicalName = datasetEntry["canonicalName"],
              application = datasetEntry["application"],
              tenant = datasetEntry["tenant"],
              versionName = datasetEntry["versionName"],
              schema = datasetEntry["schema"],
              inputDatasets = inputDatasets,
              context = datasetEntry["context"])

            dataset.id = datasetEntry["id"]

            return dataset


        return None



    def get_artifacts(self,
      dataset: Dataset,
      from_time: datetime.datetime = None,
      to_time: datetime.datetime = None,
      limit: int = None) -> List[DataArtifact]:
        # first check with model store yada-yada
        evaluation = None
        evaluationMetaArtifact = None

        meta = {
            "artifactType": "dataArtifact",
            "canonicalName": dataset.canonicalName,
            "datasetId": dataset.id
        }

        # convert times to utc timezone
        from_utc = from_time.astimezone(datetime.timezone.utc) if from_time else None
        to_utc = to_time.astimezone(datetime.timezone.utc) if to_time else None

        data_artifacts_meta = self._get_dataset_meta(meta, from_time=from_utc, to_time=to_utc, limit=limit)
        data_artifacts = []


        for artifact_meta in data_artifacts_meta or []:
            a = self._dict_to_artifact(artifact_meta)
            data_artifacts.append(a)


        return data_artifacts





    def load_artifacts(self, artifact_type: Type[Any], artifacts: List[DataArtifact]) -> Any:

        # get materializer by type
        materializer:DataFrameMaterializer = self.get_materializer(artifact_type)
        loaded_artifacts = materializer.load(artifact_type, artifacts)

        # track loaded artifacts to use them for lineage for saving new artifacts

        return loaded_artifacts






    # methods to publish datasets as data artifacts
    def save(self, dataframe: Any, data_artifact: DataArtifact, options:Dict[str, Any] = None) -> DataArtifact:


        # prepare data artifact
        # ...
        ref:str = (data_artifact.application + "/"
            + (data_artifact.target + "/") if data_artifact.target else ""
            + data_artifact.datasetId + "/"
            + data_artifact.pipelineName + "/"
            + data_artifact.pipelineStage + "/"
            + data_artifact.pipelineRunId + "/"
            + uuid.uuid4())


        hash_enc:str = hashlib.md5(ref).hexdigest()
        data_refpath:str = self.context.get_repo_uri() + "/" + hash_enc[:4] + "-" + ref

        data_ref:DataRef = DataRef(data_refpath, self.context.store_type)

        #copy artifact and assign new data ref
        copy_artifact = pickle.loads(pickle.dumps(data_artifact))
        copy_artifact.artifactRef = data_ref

        # get materializer by type
        materializer:DataFrameMaterializer = self.get_materializer(type(dataframe))
        # now save in blobstore and in metadata
        materializer.save(dataframe, copy_artifact, options)
        return self.put_data_artifact(copy_artifact)



    def create_dataset(self, dataset: Dataset) -> Dataset:
        ds = self.put_dataset(dataset)
        return ds





    def put_data_artifact(self, artifact: DataArtifact) -> DataArtifact:
        return self.put_artifact(artifact)

    def put_dataset(self, dataset: Dataset) -> Dataset:
        return self.put_artifact(dataset)

    def put_artifact(self, artifact: ArtifactMeta) -> ArtifactMeta:

        # post model metadata

        artifact_meta_type:str = "dataset"
        if isinstance(artifact, DataArtifact):
            artifact_meta_type = "dataArtifact"


        reqMeta = urllib.request.Request(DATASTORE_API + "/v1.0/genome/" + artifact_meta_type)
        reqMeta.add_header(
            'Content-Type',
            'application/json',
        )


        try:
            responseMeta = urllib.request.urlopen(reqMeta, artifact.to_json().encode('utf-8'))
            data = responseMeta.read()

            artifact_meta_resp = json.loads(data)
            logging.info(artifact_meta_type + "-id: " + str(artifact_meta_resp["id"]))

            #return artifact with newly assigned id
            copy_artifact = pickle.loads(pickle.dumps(artifact))
            copy_artifact.id = str(artifact_meta_resp["id"])
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
