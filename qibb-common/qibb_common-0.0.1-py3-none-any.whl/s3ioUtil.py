# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:15:48 2023

@author: Himanshu
"""

import boto3
import pandas as pd
import os
import io

class S3IO:
    """
    Class to handle any external S3 based input output
    """

    def __init__(self, access_key, secret_key):
        '''
        Constructor
        '''
        self.s3client = boto3.client(
           's3',
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key)
    
    
    
    def get_list_of_files(self, bucket, prefix_path):
        """
        Get List of files in a S3 Location using user provide external_properties
        List files in specific S3 URL
        """
        file_list = []
        #Paginated results to download png files
        paginator = self.s3client.get_paginator('list_objects')
        operation_parameters = {'Bucket': bucket,
                                'Prefix': prefix_path}
        page_iterator = paginator.paginate(**operation_parameters)
        pCount = 0
        for page in page_iterator:
            pCount = pCount + 1
            print("extracting page " + str(pCount))
            pgList = []#cont['Key'] for cont in page['Contents']]
            for cont in page['Contents']:
                if cont['Key'].endswith('/') is False:
                    pgList.append(cont['Key'])
            
            file_list = file_list + pgList
            
        return file_list
    
    
    def get_file_as_dataframe(self, bucket, file_path):
        """
        Get a CSV file in S3 as dataframe
        """
        obj = self.s3client.get_object(Bucket = bucket , 
                             Key = file_path)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()), 
                         encoding='utf8',sep=',')
        return df
    
    
    def download_file(self, bucket, file_path, out_dir=''):
        """
        Download file in S3 as local file
        """
        
        if out_dir == '':
            out_file = os.path.basename(file_path)
            
        else:
            out_file = os.path.join(out_dir, os.path.basename(file_path))
            
            if os.path.exists(out_dir) is False:
                print('Creating out_dir ' + out_dir)
                os.mkdir(out_dir)
                
        print('Downloading ' + out_file)
        
        self.s3client.download_file(Bucket = bucket , 
                             Key = file_path, Filename=out_file)
        return
    
    """
    Upload a file in a S3 Location using user provided external_properties
    """
    def upload_file(self, bucket, localFileName, outFileName, overwrite=False):
        if self.s3client.obj
        
        print('uploading to ' + outFileName)
        self.s3client.upload_file(localFileName, bucket, outFileName)
        
#Test
# config = {
#         "access_key":"AKIA2KXYWVN73GPF5PKF",
#         "secret_key":"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",
#         "Bucket":"qibb-test",
#         "destination_folder":"getDataInformation",
#         "wfid": 2,
#         "time": "2023-1-3T17:11:04",
#         "prev_nodes_list": ["s3 Ingestor"]
#     }
# s3io = S3IO(config['access_key'], config['secret_key'])
# print(s3io.get_list_of_files(
#     config['Bucket'], 
#     prefix_path='qiworkflow_2_2023-1-3T17:11:04/s3 Ingestor'))

# file_path = 'qiworkflow_2_2023-1-3T17:11:04/s3 Ingestor/demo.csv'
# df = s3io.get_file_as_dataframe(config['Bucket'], file_path)
# print(df.shape)

# s3io.download_file(config['Bucket'], 
#                    file_path, 
#                    out_dir='tmp')

# s3io.upload_file(config['Bucket'], 
#                  localFileName='tmp/demo.csv', 
#                  outFileName= 'demo.csv')
