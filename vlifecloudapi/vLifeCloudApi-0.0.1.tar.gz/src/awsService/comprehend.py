from awsService import helper
import boto3

comprehendClient = boto3.client('comprehend','us-east-1')

'''
# fileType either S3 or LOCAL or TEXT
def getData(bucketName=None, fileKey=None, fileType=None, text=None):
    try:
        if fileType == 'S3' and bucketName != None and fileKey != None:
            data = helper.readS3File(bucketName, fileKey)
        elif fileType == 'LOCAL' and fileKey != None:
            data = helper.readLocalFile(fileKey)
        else:
            # File type as String
            data = text

    except BaseException as error:
       return error

    return data 
'''

def detect_entities(bucketName=None, fileKey=None, fileType=None, text=None): 

    # Fetch Data from multiple source
    data=helper.getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = comprehendClient.detect_entities(
                    Text=data,
                    LanguageCode='en')
    except BaseException as error:
        return error

    return response
        

def detect_key_phrases(bucketName=None, fileKey=None, fileType=None, text=None):

    # Fetch Data from multiple source
    data=getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = comprehendClient.detect_key_phrases(
                    Text=data,
                    LanguageCode='en')
    except BaseException as error:
        return error 

    return response    

def detect_pii_entities(bucketName=None, fileKey=None, fileType=None, text=None):

    # Fetch Data from multiple source
    data=getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = comprehendClient.detect_pii_entities(
                    Text=data,
                    LanguageCode='en')
    except BaseException as error:
        return error

    return response

def detect_sentiment(bucketName=None, fileKey=None, fileType=None, text=None):

    # Fetch Data from multiple source
    data=getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = comprehendClient.detect_sentiment(
                    Text=data,
                    LanguageCode='en')
    except BaseException as error:
        return error 


    return response        


