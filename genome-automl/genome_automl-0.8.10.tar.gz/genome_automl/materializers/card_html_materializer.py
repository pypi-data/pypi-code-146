from typing import Mapping, List, Tuple, Dict, Type, Union, Any
from enum import Enum

from ..base import BaseRef, DataRef, Dataset, DataArtifact, ModelArtifact
from ..card import Card, CardArtifact

from .factory import CardMaterializer, DataFrameMaterializer, DataFormat, NoFormatSupport

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
    from matplotlib import pyplot as plt
    import markdown
except ImportError:
    warnings.warn('markdown or matplotlib could not be imported', ImportWarning)


MODELSTORE_API = os.getenv('BLOBSTORE') or os.getenv('GENOMESTORE')


class CardHTMLMaterializer(CardMaterializer):

    SUPPORTED_TYPES = (Card, )


    def __init__(self):

        super().__init__()


    # save Cards in the provided format
    def save_to_ref(self, card: Any,
                          format: DataFormat,
                          base_ref: BaseRef,
                          options:Dict[str, Any] = None) -> None:


        blobstore_api: str = options["blob_api"] if options and "blob_api" in options else MODELSTORE_API


        # store in blobstore
        blob_id:str = self._create_blobstore_blob(card.to_html().encode('utf-8'), blobstore_api)

        #change base ref to point to blob id
        base_ref.ref = blob_id
        base_ref.refType = "modelstore"
