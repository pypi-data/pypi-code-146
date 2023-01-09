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


import warnings
from typing import Mapping, List, Tuple, Dict, Union, Type, Any


from .base import BaseRef, CodeRef, DataRef, Segment, ArtifactMeta, Dataset, DataArtifact, BaseMetric
from .materializers.factory import MaterializerRegistry, Materializer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)




class StoreContext():

    def __init__(self, bucket:str = None, store_type:str = None):
        self.bucket = bucket
        self.store_type = store_type if store_type in ['s3', 'gs', 'local'] else 'local'

    def get_repo_uri(self) -> str:

        prefix = {"s3": "s3://", "gs":"gs://", "local": "file://"}
        return prefix[self.store_type] + self.bucket



class Store():

    def __init__(self, context: StoreContext):

        self.context = context


    def _get_artifact_code(self, prop:str, artifact_meta: Dict[str, Any]) -> CodeRef:

        code_ref: CodeRef = None
        if prop in artifact_meta:
            code_dict:Dict[str, str] = artifact_meta[prop]
            if code_dict and "ref"  in code_dict and "refType" in code_dict:
                code_ref = CodeRef( code_dict["ref"], code_dict["refType"])
                if "version" in code_dict:
                    code_ref.version = code_dict["version"]


        return code_ref


    def register_materializer(self, materializer: Materializer) -> None:
        MaterializerRegistry.register_materializer(materializer)

    def get_materializer(self, artifact_type: Type[Any]) -> Materializer:
        return MaterializerRegistry.get_materializer(artifact_type)
