# -*- coding: utf-8 -*-
from .bp import *
from .svc import *
from .dmo import *

from .find_s3_file import FindS3File
from .find_owl_file import FindOwlFile
from .find_jpg_file import FindJpgFile


def find_ontology(file_name: str) -> dict:
    return FindOwlFile(file_name=file_name).process()
