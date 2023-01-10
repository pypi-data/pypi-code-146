import logging
import argh
from doc2tei import _process_doc
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def _convert_file(input_file_path: str, keep_transient_files: bool = True):
    """
    Converts a *.docx file to XML TEI.
    """
    _process_doc(input_file_path, os.getcwd(), logger, keep_transient_files)


argh.dispatch_command(_convert_file)
