
from typing import TYPE_CHECKING

from .annotation import Annotation
from .constants import OPERATION_MODE_AUTO
from .logger import get_debug_logger


if TYPE_CHECKING:
    from . import DatalakeClient

model_logger = get_debug_logger('Model')


class ModelRun(Annotation):
    def __init__(self, client: "DatalakeClient"):
        super().__init__(client)

    def upload_modelrun_json(self, storage_base_path: str, model_id: str, file_path: str, annotation_geometry: str, is_normalized: bool):
        model_logger.debug(f'Started uploading model run data for model_id: {model_id}')
        self.upload_annotation_json(storage_base_path, model_id, file_path, annotation_geometry, OPERATION_MODE_AUTO, is_normalized)
        model_logger.debug(f'Finished uploading model run data for model_id: {model_id}')

