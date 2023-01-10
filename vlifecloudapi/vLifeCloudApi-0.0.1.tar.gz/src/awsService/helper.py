import boto3

s3Client = boto3.resource('s3')

# fileType either S3 or LOCAL or TEXT
def getData(bucketName=None, fileKey=None, fileType=None, text=None):
    try:
        if fileType == 'S3' and bucketName != None and fileKey != None:
            data = readS3File(bucketName, fileKey)
        elif fileType == 'LOCAL' and fileKey != None:
            data = readLocalFile(fileKey)
        else:
            # File type as String
            data = text

    except BaseException as error:
        return error

    return data

def readS3File(bucketName, fileKey):
    
    keyObj = s3Client.Object(bucketName, fileKey)
    body = keyObj.get()['Body'].read()
    #Convert bytes to String
    data=body.decode("utf-8")

    return data 

def readLocalFile(fileKey):

    with open(fileKey, 'r') as file:
        data = file.read().replace('\n', '')

    return data



