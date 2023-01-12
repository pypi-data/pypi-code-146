import base64

from layerx.datalake.annotation import Annotation

from .ground_truth import GroundTruth
from .constants import BOX_ANNOTATION, POLYGON_ANNOTATION, LINE_ANNOTATION, MediaType
from .datalakeinterface import DatalakeInterface
from .file_upload import FileUpload
from .logger import get_debug_logger
from .model_run import ModelRun

datalake_logger = get_debug_logger('DatalakeClient')


class DatalakeClient:
    """
    Python SDK of Datalake
    """

    def __init__(self, encoded_key_secret: str, layerx_url: str) -> None:
        _datalake_url = f'{layerx_url}/datalake'
        self.datalake_interface = DatalakeInterface(encoded_key_secret, _datalake_url)

    def upload_annotation_from_cocojson(self, file_path: str):
        """
        available soon
        """
        datalake_logger.debug(f'file_name={file_path}')
        _annotation = GroundTruth(client=self)
        _annotation.upload_coco(file_path)

    def upload_modelrun_from_json(
            self,
            storage_base_path: str,
            model_id: str,
            file_path: str,
            annotation_geometry: str,
            is_normalized: bool
    ):
        datalake_logger.debug(f'upload_modelrun_from_json file_path={file_path}, '
                              f'annotation_geometry={annotation_geometry}')
        _model = ModelRun(client=self)
        if annotation_geometry == BOX_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, BOX_ANNOTATION, is_normalized)
        elif annotation_geometry == POLYGON_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, POLYGON_ANNOTATION, is_normalized)
        elif annotation_geometry == LINE_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, LINE_ANNOTATION, is_normalized)
        else:
            datalake_logger.debug(f'unsupported annotation_geometry={annotation_geometry}')

    def upload_groundtruth_from_json(
            self,
            storage_base_path: str,
            operation_id: str,
            file_path: str,
            annotation_geometry: str,
            is_normalized: bool
    ):
        datalake_logger.debug(f'upload_groundtruth_from_json file_path={file_path}, '
                              f'annotation_geometry={annotation_geometry}')
        _groundTruth = GroundTruth(client=self)
        if annotation_geometry == BOX_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, BOX_ANNOTATION, is_normalized)
        elif annotation_geometry == POLYGON_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, POLYGON_ANNOTATION, is_normalized)
        elif annotation_geometry == LINE_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, LINE_ANNOTATION, is_normalized)
        else:
            datalake_logger.debug(f'unsupported annotation_geometry={annotation_geometry}')

    def file_upload(self, path: str, collection_type, collection_name, meta_data_object, override):
        _upload = FileUpload(client=self)
        _upload.file_upload_initiate(path, collection_type, collection_name, meta_data_object, override)

    def get_upload_status(self, collection_name):
        _upload = FileUpload(client=self)
        return _upload.get_upload_status(collection_name)

    def remove_collection_annotations(self, collection_id: str, model_run_id: str):
        print(f'annotation delete of collection ={collection_id}', f'model id={model_run_id}')
        _model = Annotation(client=self)
        _model.remove_collection_annotations(collection_id, model_run_id)



