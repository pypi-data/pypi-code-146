"""This module interacts with /presign api of infer-node-api to generate
presigned urls for file upload and download
"""

from deeplabel.client import BaseClient

def get_upload_url(key:str, client:BaseClient) -> str:
    """Given an s3 presigned url to upload the key
    Used internally for uploading analytics images to gallery after infer, etc
    """
    params = dict(key=key, method="put")
    resp = client.get('/presign', params)
    return resp.json()['data']

def get_download_url(key:str, client:BaseClient) -> str:
    """Get presigned GET url for files uploaded using get_upload_url
    Used internally for uploading analytics images to gallery after infer, etc
    """
    params = dict(key=key, method='get')
    resp = client.get('/presign', params)
    return resp.json()['data']