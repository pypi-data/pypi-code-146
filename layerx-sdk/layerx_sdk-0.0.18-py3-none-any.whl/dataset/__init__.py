from .sync import DatasetSync


class DatasetClient:
    """
    Python SDK of Dataset download
    """
    def __init__(self, encoded_key_secret: str, layerx_url: str) -> None:
        self._dataset_sync_tool = DatasetSync(encoded_key_secret, layerx_url)

    """
    Download dataset
    @param version_id - id of dataset version 
    @param export_type - dataset export format """
    def download_dataset(self, version_id: str, export_type: str):
        self._dataset_sync_tool.download_dataset(version_id, export_type)

    """
    Download collection annotations
    From datalake
    @param collection_id - id of dataset version
    @param model_id - Optional: id of the model (same operation_id given in upload annotations) 
    if we need annotations for that specific model """
    def download_annotations(self, collection_id: str, model_id: str):
        self._dataset_sync_tool.download_collection(collection_id, model_id)
