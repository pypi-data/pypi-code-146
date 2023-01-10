import os
from google.cloud import storage
from dotenv import load_dotenv

storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024* 1024  # 10 MB. Increase this when network speed is high. Decrease in low speed network to prevent failure
PROJECT_ID = "mlops-315607"
global_storage_client = storage.Client(PROJECT_ID)

def _upload_blob(args):
    blob_name, datasetname, location, metadata = args 
    storage_client = storage.Client(PROJECT_ID)
    bucket = storage_client.bucket("datasets-{}".format(datasetname))

    if not bucket.exists():
        raise Exception("Dataset bucket not found")
        
    blob = bucket.blob(blob_name)
    if metadata is not None:
        blob.metadata = metadata
    # blob._chunk_size = 5*1024*1024
    blob.upload_from_filename(os.path.join(location, blob_name))
    if blob.exists():
        return blob_name

def _download_blob(args):
    blob_name, datasetname, save_to = args
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("datasets-{}".format(datasetname))

    if not bucket.exists():
        raise Exception("Dataset bucket not found")
        
    blob = bucket.get_blob(blob_name)
    blob.download_to_filename(os.path.join(save_to, blob_name))
    return blob_name

def list_blob(bucket_name):
    bucket = global_storage_client.bucket(bucket_name)
    if not bucket.exists():
        raise Exception("Dataset bucket not found")
    return list(bucket.list_blobs())

def get_bucket_name(dataset_name):
    return "datasets-{}".format(dataset_name)
