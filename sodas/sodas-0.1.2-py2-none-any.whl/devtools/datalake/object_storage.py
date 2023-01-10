import json
import requests
import boto3

from sodas.devtools.gateway import auth
from sodas.devtools.distribution import dataset, distribution
from sodas.devtools.datalake import credential

# Distribution에 등록된 object에 접근하기 위해 필요한 config를 return 함.
def _get_config_for_object_in_distribution (
        base_url: str,
        id: str,
        refresh_token: str,
        file_name: str,
        end_point: str
    ):
    
    access_token = auth._get_access_token(base_url, id, refresh_token)
    
    dataset_list = dataset._get_dataset_list(base_url, access_token)
    dataset_id = dataset._find_dataset_id(dataset_list)
    
    distribution_list = distribution._get_distribution_list(base_url, access_token, dataset_id)
    distribution_id = distribution._find_distribution_id(distribution_list, file_name)
    distri_ = distribution._get_distribution(base_url, access_token, distribution_id)
    
    object_name = distribution._find_file_name(distri_)
    bucket_name = distribution._find_bucket_name(distri_)
    
    credential_list = credential._get_credential_object_storage(base_url, access_token, end_point)
    access_key, secret_key = credential._get_credential_key(credential_list)
    
    return object_name, bucket_name, access_key, secret_key

# Object storage에 접근하기 위해 필요한 config를 return 함
def _get_config_for_object(
        base_url: str,
        id: str,
        refresh_token: str,
        end_point: str,
    ):
    
    access_token = auth._get_access_token(base_url, id, refresh_token)
    credential_list = credential._get_credential_object_storage(base_url, access_token, end_point)
    access_key, secret_key = credential._get_credential_key(credential_list)
    bucket_name = id.replace('_', '')
    
    return bucket_name, access_key, secret_key

def get_object_in_distribution(
        base_url: str,
        id: str,
        refresh_token: str,
        file_name: str,
        end_point: str
    ) -> object:
    """Distribution 내에 등록되어 있는 object를 read하는 함수

    Args:
        base_url (str): Base URL 
        id (str): SODAS+ User ID
        refresh_token (str): SODAS+ User Refresh Token
        file_name (str): Distribution File Name
        end_point (str): Distribution Endpoint

    Returns:
        Object: Object File
    """
    object_name, bucket_name, access_key, secret_key = _get_config_for_object_in_distribution(
                                                                        base_url,
                                                                        id,
                                                                        refresh_token,
                                                                        file_name,
                                                                        end_point
                                                                    )
    
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = end_point,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        res = s3.get_object(Bucket=bucket_name, Key=object_name)
        status = res.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 get_object response. Status - {status}")
            return res.get("Body")
        else:
            print(f"Unsuccessful S3 get_object response. Status - {status}")
    except Exception as e:
        print(e)

def get_object_list (
        base_url: str,
        id: str,
        refresh_token: str,
        end_point: str
    )-> dict:
    """User의 object storage에 저장된 objects의 list를 얻는 함수

    Args:
        base_url (str): Base URL 
        id (str): SODAS+ User ID
        refresh_token (str): SODAS+ User Refresh Token
        end_point (str): Distribution Endpoint

    Returns:
        dict: Dictionary of Object List
    """
    bucket_name, access_key, secret_key = _get_config_for_object(base_url, id, refresh_token, end_point)
    
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = end_point,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        res = s3.list_objects(Bucket = bucket_name)
        status = res.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 get_object response. Status - {status}")
            keys = res['Contents']
            return keys
        else:
            print(f"Unsuccessful S3 get_object response. Status - {status}")
    except Exception as e:
        print(e)
        
        
def get_object(
        base_url: str,
        id: str,
        refresh_token: str,
        file_name: str,
        end_point: str
    ) -> object:
    """Object storage에 저장된 object를 read하는 함수 (Distribution에 등록되어 있지 않더라도 object storage 내에 있는 모든 object에 접근할 수 있음)

    Args:
        base_url (str): Base URL 
        id (str): SODAS+ User ID
        refresh_token (str): SODAS+ User Refresh Token
        file_name (str): Object Name
        end_point (str): Distribution Endpoint


    Returns:
        object: Object File
    """
    
    bucket_name, access_key, secret_key = _get_config_for_object(base_url, id, refresh_token, end_point)
    
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = end_point,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        res = s3.get_object(Bucket=bucket_name, Key=file_name)
        status = res.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 get_object response. Status - {status}")
            obj = res.get("Body")
            return obj
        else:
            print(f"Unsuccessful S3 get_object response. Status - {status}")
    except Exception as e:
        print(e)
        
def save_object(
        base_url: str,
        id: str,
        refresh_token: str,
        file_name: str,
        end_point: str
    ):
    """Object storage에 object를 save하는 함수.

    Args:
        base_url (str): Base URL 
        id (str): SODAS+ User ID
        refresh_token (str): SODAS+ User Refresh Token
        file_name (str): Local File Name
        end_point (str): Object Endpoint

    """
    
    bucket_name, access_key, secret_key = _get_config_for_object(base_url, id, refresh_token, end_point)

    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = end_point,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        response = s3.upload_file(file_name, bucket_name, file_name)
        
    except Exception as e:
        print(e)
        
def override_object_in_distribution(
        base_url: str,
        id: str,
        refresh_token: str,
        local_file_name: str,
        distribution_file_name: str,
        end_point: str
    ):
    """Distribution에 등록된 object에 덮어 씌우는 함수. 

    Args:
        base_url (str): Base URL 
        id (str): SODAS+ User ID
        refresh_token (str): SODAS+ User Refresh Token
        local_file_name (str): Local File Name
        distribution_file_name (str): Distribution File Name,
        end_point (str): Distribution Endpoint
        
    Returns:
        _type_: _description_
    """
    
    object_name, bucket_name, access_key, secret_key = _get_config_for_object_in_distribution(
                                                                    base_url,
                                                                    id,
                                                                    refresh_token,
                                                                    distribution_file_name,
                                                                    end_point
                                                                )  
    
    try:
        s3 = boto3.client(
        's3',
        '',
        use_ssl = False,
        verify = False,
        endpoint_url = end_point,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
        )
        
        response = s3.upload_file(local_file_name, bucket_name, object_name)
        
    except Exception as e:
        print(e)