from awsService import helper
import boto3

medicalComprehendClient = boto3.client('comprehendmedical','us-east-1')


def detect_entities_v2(bucketName=None, fileKey=None, fileType=None, text=None): 

    # Fetch Data from multiple source
    data=helper.getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = medicalComprehendClient.detect_entities_v2(
                    Text=data)
    except BaseException as error:
        return error 

    return response

def detect_phi(bucketName=None, fileKey=None, fileType=None, text=None): 

    # Fetch Data from multiple source
    data=helper.getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = medicalComprehendClient.detect_phi(
                    Text=data)
    except BaseException as error:
        return error 

    return response   

def infer_icd10_cm(bucketName=None, fileKey=None, fileType=None, text=None): 

    # Fetch Data from multiple source
    data=helper.getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = medicalComprehendClient.infer_icd10_cm(
                    Text=data)
    except BaseException as error:
        return error 

    return response   

def infer_rx_norm(bucketName=None, fileKey=None, fileType=None, text=None): 

    # Fetch Data from multiple source
    data=helper.getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = medicalComprehendClient.infer_rx_norm(
                    Text=data)
    except BaseException as error:
        return error 

    return response  

def infer_snomedct(bucketName=None, fileKey=None, fileType=None, text=None): 

    # Fetch Data from multiple source
    data=helper.getData(bucketName=bucketName, fileKey=fileKey, fileType=fileType, text=text)

    try:
        response = medicalComprehendClient.infer_snomedct(
                    Text=data)
    except BaseException as error:
        return error 

    return response       