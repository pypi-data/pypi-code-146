import base64
from re import S

from layerx import datalake, dataset
from layerx.datalake.constants import MediaType


class LayerxClient:
    """
    Python SDK of LayerX
    """

    def __init__(self, api_key: str, secret: str, layerx_url: str) -> None:
        _string_key_secret = f'{api_key}:{secret}'
        _key_secret_bytes = _string_key_secret.encode("ascii")
        _encoded_key_secret_bytes = base64.b64encode(_key_secret_bytes)
        self.encoded_key_secret = _encoded_key_secret_bytes.decode("ascii")
        self.layerx_url = layerx_url

    def upload_annoations_for_folder(
            self,
            collection_base_path: str,
            operation_unique_id: str,
            json_data_file_path: str,
            shape_type: str,
            is_normalized: bool,
            is_model_run: bool
    ):
        """
        Upload annotation data from a json file
        """
        # init datalake client
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)

        if is_model_run:
            _datalake_client.upload_modelrun_from_json(
                collection_base_path,
                operation_unique_id,
                json_data_file_path,
                shape_type,
                is_normalized
            )
        else:
            _datalake_client.upload_groundtruth_from_json(
                collection_base_path,
                operation_unique_id,
                json_data_file_path,
                shape_type,
                is_normalized)

    """
    Download dataset """

    def download_dataset(self, version_id: str, export_type: str):
        # init dataset client
        _dataset_client = dataset.DatasetClient(self.encoded_key_secret, self.layerx_url)

        # start download
        _dataset_client.download_dataset(version_id, export_type)

    """"
    Images/vidoe upload
    """

    def file_upload(self, path: str, collection_type, collection_name, meta_data_object="", override=False):
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        _datalake_client.file_upload(path, collection_type, collection_name, meta_data_object, override)

    """
    Download collection annotations
    From datalake
    @param collection_id - id of dataset version
    @param model_id - Optional: id of the model (same operation_id given in upload annotations) 
    if we need annotations for that specific model """

    def download_annotations(self, collection_id: str, model_id: str):
        # init dataset client
        _dataset_client = dataset.DatasetClient(self.encoded_key_secret, self.layerx_url)

        # start download
        _dataset_client.download_annotations(collection_id, model_id)
    

    """"
    Images and annotation upload
    """
    def upload_data(self, collection_name, file_path, meta_data_object, operation_unique_id, json_data_file_path, shape_type, is_normalized, is_model_run):

        if (file_path == None):
            print('file upload cannot be done')
        else:
            self.file_upload(file_path, MediaType.IMAGE.value, collection_name, meta_data_object, False)

        if (json_data_file_path == None):
            print('annotation upload cannot be done')
        else:
            self.upload_annoations_for_folder(collection_name, operation_unique_id, json_data_file_path, shape_type, is_normalized, is_model_run)
    


    """"
    get upload progress
    """

    def get_upload_status(self, collection_name):
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        return _datalake_client.get_upload_status(collection_name)

    """
    remove annotations of collection model run
    """
    def remove_annotations(self, collection_id: str, model_run_id: str):
        print(f'remove annotations of collection: {collection_id}, operation id: {model_run_id}')

        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)

        _datalake_client.remove_collection_annotations(collection_id, model_run_id)
        

