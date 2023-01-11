"""s3 related module"""

#############################
###### import packages ######
#############################

import boto3
import io

##########################
###### create class ######
##########################

# example of key id https://d-9067613818.awsapps.com/start#/
# aws_access_key_id='ASIAXX5SD4DTFG5YRLX7'
# aws_secret_access_key='FjGsVqZrmnVbmEts7EmN7n7R8pqfwi7vFEP7QZAG'
# aws_session_token='IQoJb3JpZ2luX2VjECgaCXVzLWVhc3QtMSJHMEUCIBAYuTl5OHvTrNK5CCcZiuY/AjOso6vY4+Yuzhb6ZYbmAiEA7V3R3Azh8u2zYhBnrJi3oICmwmm3weioJGmaf7k7zwwqkwMIof//////////ARABGgw1MzI0MTI2MjEwMzAiDKraE33cw2xeQfZm6irnAh+npfjd1sWi+kpTc1WLuzT/lMj51MLA3W4CaNX/FebViHdtwPSFCvXzxHcuOb6igQOoZyy1+fWqorNCM5fuj1NFlzljS+Xtmb84SUpwAV/mJGHAjl4nZE11eop1UZytvE+fFoThpKz8rmZW0r3oEh8BqyCI9sqvYM3E8LadOngOExNo3VujXS0S79Eetpgr7b1PqT8rMj2VrFLJPq+T+W1juUuCBqDnHpoM4wEsXIZdKGKGsWR9b2eR4pnsO8bAoZew86dx2GFjZ0MSC7vY075nlLsM7KgENtVCHdlYUzjs9JE5/5h+9tdQAcFn9tp+6yXp2ZWdnshwA/XWthH0gJPlDYp707hELPd3lvl1QTwtIkvjhFjETccRt6EkBYq0BRMyge4cABG/EFH29RpCR19DJtl2h1Q6lZSMBFjOxBPEWd+z7DlpH6QQ/j7qbAlPC4frZvdORRhm8osXFqLtvtpwoChp1O1zMNGxl5gGOqYBNboeGsg+0solaFHZtxg3sx9Z2ZF2j/BWf4st5DHpLxurWy/i/kKBkwi16ZjbNqyMl1wWKupoBpmELMpJuJLpXftKTnadK1jcMAMEmX8H5fSjY1uJCwruWSHxC2piSo1dregxgZH/aF0pxIK4V/fP/SpvAtGfN2DCt0kFtmrm4waLG0diC/RYBjm4fL7b1EmJC3bLw02LBYC3dpTRUUNLCtgUEoRtkw=='

class ConnS3:
    """Class for S3"""
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_session_token):
        self.aws_id =  aws_access_key_id
        self.aws_key = aws_secret_access_key
        self.aws_token = aws_session_token

        # create session
        if (self.aws_id is not None) & (self.aws_key is not None) & (self.aws_token is not None):
            self.s3_session = boto3.Session(
                aws_access_key_id = self.aws_id,
                aws_secret_access_key = self.aws_key,
                aws_session_token = self.aws_token,
            ) # create aws session if there is aws credential defined
        else:
            self.s3_session = boto3.Session() # create aws session using using environment detail 

    def s3_list_bucket(self):
        """list bucket inside s3"""
        s3_resource = self.s3_session.resource('s3') # create s3 resource
        buckets = [bucket.name for bucket in s3_resource.buckets.all()] # list down the bucket
        return buckets

    def s3_list_all_file_folder(self, s3_bucket_def):
        """list files inside bucket s3"""
        s3_resource = self.s3_session.resource('s3') # create s3 resource
        my_bucket = s3_resource.Bucket(s3_bucket_def) # define the bucket
        file = [file for file in my_bucket.objects.all()]
        return file

    def s3_list_file_folder_in_path(self, s3_bucket_def, s3_prefix_def):
        """list files inside bucket s3 and specific prefix"""
        s3_client = self.s3_session.client('s3') # create s3 resource
        response = s3_client.list_objects_v2(
                    Bucket = s3_bucket_def
                    , Prefix = s3_prefix_def
                    , Delimiter = "/"
                    )
        content = [content.get('Key') for content in response.get('Contents', [])]
        file = [file for file in content]
        content = [content.get('Prefix') for content in response.get('CommonPrefixes', [])]
        folder = [file for file in content]
        return file, folder

    def s3_list_all_file_folder_in_path(self, s3_bucket_def, s3_prefix_def):
        """list files inside bucket s3 and specific prefix"""
        s3_client = self.s3_session.client('s3') # create s3 resource
        response = s3_client.list_objects_v2(
                    Bucket = s3_bucket_def
                    , Prefix = s3_prefix_def
                    )
        content = [content.get('Key') for content in response.get('Contents', [])]
        file = [file for file in content]
        content = [content.get('Prefix') for content in response.get('CommonPrefixes', [])]
        folder = [file for file in content]
        return file, folder

    def s3_upload_file(self, s3_bucket_def, s3_file_def, df_def):
        """list files inside bucket s3"""
        s3_client = self.s3_session.client('s3') # create aws client
        with io.BytesIO() as parquet_buffer:
            df_def.to_parquet(parquet_buffer, index=False) # expoet pandas to parquet
            response = s3_client.put_object(
                Bucket = s3_bucket_def
                , Key = s3_file_def
                , Body = parquet_buffer.getvalue()
                ) # put object inside bucket and file path
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
            if status == 200:
                print(f"Successful S3 put_object response. Status - {status}") # status if success
            else:
                print(f"Unsuccessful S3 put_object response. Status - {status}") # status if not success
