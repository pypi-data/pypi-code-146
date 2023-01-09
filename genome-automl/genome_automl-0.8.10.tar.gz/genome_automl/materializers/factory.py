from ..base import BaseRef, DataRef, Dataset, DataArtifact, ModelArtifact, ArtifactMeta
from ..card import Card, CardArtifact

from typing import Mapping, List, Tuple, Dict, Type, Any
from enum import Enum

import json
import logging
import sys
import time
import os
import os.path
import pickle
import urllib.request
from urllib.error import  URLError

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class NoMaterializerSupportForType(Exception):
    pass

class NoFormatSupport(Exception):
    pass

class DataFormat(Enum):
    PARQUET = "parquet"
    JSON = "json"
    CSV = "csv"
    AVRO = "avro"
    SAVED_MODEL = "saved_model"
    HTML = "html"




class Materializer():

    SUPPORTED_TYPES = ()


    def _is_supported_type(self, data_type: Type[Any]) -> bool:

        return any(
            issubclass(data_type, supported_type) for supported_type in self.SUPPORTED_TYPES
        )


    def _get_artifact_format(self, artifact: Any) -> DataFormat:
        pass


    def _get_artifact_ref(self, artifact: Any) -> BaseRef:
        pass


    def _get_type(self, serializable_obj: Any) -> Type[Any]:
        return type(serializable_obj)



    def load(self, data_type:Type[Any], artifacts: List[ArtifactMeta], options:Dict[str, Any] = None) -> Any:

        # check if type is supported
        if not self._is_supported_type(data_type):
            raise NoMaterializerSupportForType(
              f"type not supported {data_type.__name__}"
              f"check materializer {self.__class__.__name__} supported types"
            )

        format = self._get_artifact_format(artifacts[0]) if len(artifacts) else None
        return self.load_ref(data_type, format, [self._get_artifact_ref(artifact) for artifact in artifacts],
               options = options)



    def load_ref(self, data_type: Type[Any], format: DataFormat, data_refs: List[BaseRef],
      options:Dict[str, Any] = None) -> Any:
        pass



    def save(self, dataframe: Any, artifact: ArtifactMeta, options: Dict[str, Any] = None) -> None:

        data_type = self._get_type(dataframe)

        if not self._is_supported_type(data_type):
            raise NoMaterializerSupportForType(
              f"type not supported {dataframe.__class__.__name__}"
              f"check materializer {self.__class__.__name__} supported types"
            )

        artifact_ref = self._get_artifact_ref(artifact)
        format = self._get_artifact_format(artifact)

        self.save_to_ref(dataframe, format, artifact_ref, options = options)




    def save_to_ref(self, dataframe: Any,
                          format: DataFormat,
                          base_ref: BaseRef,
                          options:Dict[str, Any] = None) -> None:

        pass



class DataFrameMaterializer(Materializer):

    def _get_artifact_format(self, artifact: DataArtifact) -> DataFormat:
        return DataFormat(artifact.format)

    def _get_artifact_ref(self, artifact: DataArtifact) -> BaseRef:
        return artifact.artifactRef

    def load(self, data_type: Type[Any], artifacts: List[DataArtifact], options:Dict[str, Any] = None) -> Any:
        return super().load(data_type, artifacts, options=options)

    def save(self, dataframe: Any, artifact: DataArtifact, options: Dict[str, Any] = None) -> None:
        super().save(dataframe, artifact, options=options)



class ModelMaterializer(Materializer):

    def _get_artifact_format(self, artifact: ModelArtifact) -> DataFormat:

        model_format = None

        if artifact.framework and artifact.framework.startswith("keras"):
            model_format = "saved_model"
        elif artifact.framework and artifact.framework.startswith("tensorflow"):
            model_format = "saved_model"
        elif artifact.framework and artifact.framework.startswith("sklearn"):
            model_format = "json"
        elif artifact.framework and artifact.framework.startswith("xgboost"):
            model_format = "json"
        elif artifact.framework and artifact.framework.startswith("spark"):
            model_format = "parquet"

        return DataFormat(model_format)


    def _get_artifact_ref(self, artifact: ModelArtifact) -> BaseRef:
        return artifact.artifactBlob


    # determine the type of the model or the estimator if a GenomeEstimator
    def _get_type(self, model: Any) -> Type[Any]:
        if hasattr(model, "estimator"):
            return type(model.estimator)

        return type(model)


    # stores a blob in the blobstore and returns the blob's id
    def _create_blobstore_blob(self, blob: bytes, blobstore_api: str) -> str:

        req = urllib.request.Request(blobstore_api + "/v1.0/genome/blob")
        req.add_header(
            'Content-Type',
            'application/octet-stream',
        )

        try:
            logging.info(f'reaching blob endpoint: {blobstore_api}/v1.0/genome/blob')

            response = urllib.request.urlopen(req, blob)
            data = response.read()
            model_resp = json.loads(data)


        except URLError as e:

            logging.info(f'failed to reach endpoint {blobstore_api}/v1.0/genome/blob')
            if hasattr(e, 'reason'):
                logging.info('Reason: ' + str(e.reason))

            if hasattr(e, 'code'):
                logging.info('Error code: ' + str(e.code))

            if hasattr(e, 'msg'):
                logging.info('Error message: ' + str(e.msg))

            raise e


        logging.info("created blob with blob-id: " + str(model_resp["id"]))
        return model_resp["id"]



    def load(self, data_type: Type[Any], artifacts: List[ModelArtifact], options:Dict[str, Any] = None) -> Any:
        return super().load(data_type, artifacts, options=options)

    def save(self, model: Any, artifact: ModelArtifact, options: Dict[str, Any] = None) -> None:
        super().save(model, artifact, options=options)


class CardMaterializer(Materializer):

    def _get_artifact_format(self, artifact: Any) -> DataFormat:
        return DataFormat(artifact.format)


    def _get_artifact_ref(self, artifact: Any) -> BaseRef:
        return artifact.artifactBlob


    def save(self, card: Any, artifact: CardArtifact, options: Dict[str, Any] = None) -> None:
        super().save(card, artifact, options=options)

    # stores a blob in the blobstore and returns the blob's id
    def _create_blobstore_blob(self, blob: bytes, blobstore_api: str) -> str:

        req = urllib.request.Request(blobstore_api + "/v1.0/genome/blob")
        req.add_header(
            'Content-Type',
            'application/octet-stream',
        )

        try:
            logging.info(f'reaching blob endpoint: {blobstore_api}/v1.0/genome/blob')

            response = urllib.request.urlopen(req, blob)
            data = response.read()
            model_resp = json.loads(data)


        except URLError as e:

            logging.info(f'failed to reach endpoint {blobstore_api}/v1.0/genome/blob')
            if hasattr(e, 'reason'):
                logging.info('Reason: ' + str(e.reason))

            if hasattr(e, 'code'):
                logging.info('Error code: ' + str(e.code))

            if hasattr(e, 'msg'):
                logging.info('Error message: ' + str(e.msg))

            raise e


        logging.info("created blob with blob-id: " + str(model_resp["id"]))
        return model_resp["id"]





class MaterializerRegistry():

    registered_materializers:Dict[str, Materializer] = {}

    @staticmethod
    def register_materializer(materializer: Materializer) -> None:
        MaterializerRegistry.registered_materializers[type(materializer).__name__] = materializer

    @staticmethod
    def get_materializer(artifact_type: Type[Any]) -> Materializer:

        for supported_type, materializer in MaterializerRegistry.registered_materializers.items():
            if any(
                issubclass(artifact_type, materializer_type) for materializer_type in materializer.SUPPORTED_TYPES
            ):
              return materializer


        raise NoMaterializerSupportForType(
            f"no support for type: {artifact_type.__name__} in all registered materializers"
          )


    @staticmethod
    def get_framework_materializer(framework_name: str) -> Materializer:

        for materlizer_type_name, materializer in MaterializerRegistry.registered_materializers.items():
            if framework_name in materlizer_type_name.lower():
              return materializer


        raise NoMaterializerSupportForType(
            f"no support for type: {framework_name} in all registered materializers"
          )
