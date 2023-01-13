import boto3
import pandas as pd
import os
import io

class DataIO:
    """
    Class to handle file input output based on internal properties
    """
    
    
    def __init__(self, conf):
        '''
        Constructor
        '''
        self.config = conf['internal_properties']
        self.s3client = boto3.client(
           's3',
            aws_access_key_id = self.config['access_key'],
            aws_secret_access_key = self.config['secret_key'])
    
    def get_list_of_input_files(self, input_index=0):
        """
        Get List of files in a S3 Location using internal_properties
        """
        
        prefix_path = ('qiworkflow_' + str(self.config['workflow_id']) + '_' + 
                       self.config['time'] + '/' + 
                       self.config['previous_nodes_list'][input_index])
        print('filter=' + prefix_path)
        
        """List files in specific S3 URL"""
        file_list = []
        #Paginated results to download png files
        paginator = self.s3client.get_paginator('list_objects')
        operation_parameters = {'Bucket': self.config['bucket_name'],
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
    
    
    def get_file_as_dataframe(self, file_path):
        """
        Get a CSV file in S3 as dataframe
        """
        
        obj = self.s3client.get_object(Bucket = self.config['bucket_name'] , 
                             Key = file_path)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()), 
                         encoding='utf8',sep=',')
        return df
    
    def download_file(self, file_path, out_dir=''):
        """
        Download file in file_path in S3 as local file in the out_dir
        """
        
        if out_dir == '':
            out_file = os.path.basename(file_path)
            
        else:
            out_file = os.path.join(out_dir, os.path.basename(file_path))
            
            if os.path.exists(out_dir) is False:
                print('Creating out_dir ' + out_dir)
                os.mkdir(out_dir)
                
        print('Downloading ' + out_file)
        
        self.s3client.download_file(Bucket = self.config['bucket_name'] , 
                             Key = file_path, Filename=out_file)
        return 'Download complete'
    
    def upload_file(self, localFilename, outFileName):
        """
        Write a file in a S3 Location using internal_properties
        """
        
        key = ('qiworkflow_' + str(self.config['workflow_id']) + '_' + 
                       self.config['time'] + '/' + 
                       self.config['destination_dir'] + '/' + outFileName)
        print('uploading to ' + key)
        self.s3client.upload_file(localFilename, self.config['bucket_name'], key)


#Test
# config = { "internal_properties": {
#     "access_key":"AKIA2KXYWVN73GPF5PKF",
#     "secret_key":"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",
#     "bucket_name":"qibb-test",
#     "destination_dir":"getDataInformation",
#     "workflow_id": 2,
#     "time": "2023-1-3T17:11:04",
#     "previous_nodes_list": ['s3 Ingestor']
#     }
# }
# dataio = DataIO(config)
# file_list = dataio.get_list_of_input_files()
# print(file_list)
# df = dataio.get_file_as_dataframe(file_list[0])
# print(df.shape)
# dataio.download_file(file_list[0])
# dataio.upload_file('demo.csv', 'demo.csv')