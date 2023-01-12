import json

from .keys import SESSION_ID, TOTAL_IMAGE_COUNT, UPLOADED_IMAGE_COUNT, USERNAME, LABELS, META_UPDATES_ARRAY, IS_NORMALIZED
import requests


class DatalakeInterface:

    def __init__(self, auth_token: str, dalalake_url: str):
        self.auth_token = auth_token
        self.dalalake_url = dalalake_url

    def create_datalake_label_coco(self, label, username='Python SDK'):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            USERNAME: username,
            LABELS: label,
        }
        url = f'{self.dalalake_url}/api/client/cocojson/import/label/create'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("An exception occurred")
            print(e)
        

    def find_datalake_label_references(self, label_attribute_values_dict, username='Python SDK'):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            LABELS: label_attribute_values_dict,
            USERNAME: username
        }
        url = f'{self.dalalake_url}/api/client/system/label/references'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("An exception occurred | find_datalake_label_references")
            print(e)
        

    def upload_metadata_updates(self, meta_updates, operation_type, operation_mode, operation_id, is_normalized, session_id, total_images_count, uploaded_images_count):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            META_UPDATES_ARRAY: json.dumps(meta_updates),
            SESSION_ID : session_id,
            TOTAL_IMAGE_COUNT : total_images_count,
            UPLOADED_IMAGE_COUNT : uploaded_images_count
        }

        params = {
            IS_NORMALIZED: is_normalized
        }

        url = f'{self.dalalake_url}/api/metadata/operationdata/{operation_type}/{operation_mode}/{operation_id}/update'
        print(url)

        try:
            response = requests.post(url=url, params=params, json=payload, headers=hed)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("An HTTP request exception occurred | upload metadata updates")
            print(e)
        except Exception as e1:
            print("An exception occurred in upload metadata updates")
            print(e1)
            return {"isSuccess": False}

    ''''
    Upload meta data collection
    '''

    def upload_metadata_collection(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/uploadMetadataInCollection'


        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code != 204 and status_code != 200:
                return {"isSuccess": False}
            return_object = response.json()
            return_object["isSuccess"] = True
            return return_object
        except requests.exceptions.RequestException as e:
            print("An exception occurred")
            print(e)
            return {"isSuccess": False}
        except Exception as e1:
            print("An exception occurred in upload metadata collection")
            print(e1)
            return {"isSuccess": False}

    ''''
    Get file id and key from s3 bucket
    '''

    def get_file_id_and_key(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/fileUpload/initializeMultipartUpload'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code != 204 and status_code != 200:
                return {"isSuccess": False}

            return_object = response.json()
            return_object["isSuccess"] = True
            return return_object
        except requests.exceptions.RequestException as e:
            print("An exception occurred in get_file_id_and_key")
            print(e)
            return {"isSuccess": False}
        except Exception as e1:
            print("An exception occurred in getting file id and key")
            print(e1)
            return {"isSuccess": False}

    ''''
    Get pre-signed url
    '''

    def get_pre_signed_url(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/fileUpload/getMultipartPreSignedUrls'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code != 204 and status_code != 200:
                return {"isSuccess": False}

            return_object = response.json()
            return_object["isSuccess"] = True
            return return_object
        except requests.exceptions.RequestException as e:
            print("An exception occurred in get_pre_signed_url")
            print(e)
            return {"isSuccess": False}
        except Exception as e1:
            print("An exception occurred in getting pre-signed url")
            print(e1)
            return {"isSuccess": False}


    ''''
    Finalize multipart upload
    '''

    def finalize_upload(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/fileUpload/finalizeMultipartUpload'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 204 or status_code == 200:
                return {"isSuccess": True}
            else:
                return {"isSuccess": False}
        except requests.exceptions.RequestException as e:
            print("An exception occurred in finalize_upload")
            print(e)
            return {"isSuccess": False}
        except Exception as e1:
            print("An exception occurred in finalize upload")
            print(e1)
            return {"isSuccess": False}


    def complete_collection_upload(self, upload_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/collectionUploadingStatus/{upload_id}/complete'

        try:
            response = requests.get(url=url, headers=hed)
            status_code = response.status_code
            if status_code == 204 or status_code == 200:
                return {"isSuccess": True}
            else:
                return {"isSuccess": False}
        except requests.exceptions.RequestException as e:
            print("An exception occurred in complete_collection_upload")
            print(e)
            return {"isSuccess": False}
        except Exception as e1:
            print("An exception occurred in complete collection upload")
            print(e1)
            return {"isSuccess": False}

    def get_upload_status(self, collection_name):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/collection/getuploadProgress?collectionName={collection_name}'

        try:
            response = requests.get(url=url, headers=hed)
            status_code = response.status_code
            if status_code == 204 or status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False}
        except requests.exceptions.RequestException as e:
            print(e)
            return {"isSuccess": False}
        except Exception as e1:
            print(e1)
            return {"isSuccess": False}

    def remove_modelrun_collection_annotation(self, collection_id, model_run_id, session_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/collection/deleteAnnotation?collectionId={collection_id}&operationId={model_run_id}'

        payload = {
            SESSION_ID : session_id
        }

        try:
            response = requests.get(url=url, headers=hed, json=payload)
            status_code = response.status_code
            if status_code == 204 or status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False}
        except requests.exceptions.RequestException as e:
            print("An exception occurred in delete_collection_annotation")
            print(e)
            return {"isSuccess": False}
        except Exception as e1:
            print("An exception occurred in delete_collection_annotation")
            print(e1)
            return {"isSuccess": False}

