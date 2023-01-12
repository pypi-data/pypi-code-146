import json

from .keys import USERNAME, LABELS, META_UPDATES_ARRAY
import requests


class S3Interface:

    def __init__(self):
        self.e_tag = ""

    ''''
    Upload file to the s3 bucket
    '''

    def upload_to_s3(self, url, path):

        try:
            with open(path, 'rb') as object_file:
                file_data = object_file.read()

                res = requests.put(url, data=file_data)
                self.e_tag = res.headers["ETag"][1:-1]

                return {
                    "isSuccess": True,
                    "e_tag": self.e_tag
                }
        except requests.exceptions.RequestException as e:
            print("An exception occurred in upload_to_s3")
            print(e)
            return {"isSuccess": False}

        except Exception as e1:
            print("An exception occurred in upload_to_s3")
            print(e1)
            return {"isSuccess": False}

