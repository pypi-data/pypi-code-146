import json
import os
import time
import wget
import requests
import boto3
import wget
from pathlib import Path
DATASET_LIST_URI = "/images/account/{accountId}/datasets"
DATASET_DELETE_URI = ""
DATASET_DETAILS_URI = ""
DATASET_CREATE_URI = ""
DATASET_MERGE_URI = ""

#serverUrl="http://ec2co-ecsel-14v83vt13isgk-1068401141.us-east-1.elb.amazonaws.com:8081/"
serverUrl="https://api.viena.ai/"
#serverUrl="http://192.168.1.100:8081/"

def generate_access_token_from_config_file():
    pass

def generate_access_token_from_apikey():
    if (not os.path.isfile(os.path.expanduser('~/.polygon/credentials'))):
        return "Not Found"
    f = open(os.path.expanduser('~/.polygon/credentials'), "r")
    token = f.read()
    if (token == ""):
        return "Not Found"
    token = token.split(":")
    API_KEY = token[1]

    #print(API_KEY)
    data = {'apikey': API_KEY}
    auth_headers = {'Authorization': 'Bearer ' }
    tokenUrl = serverUrl + "admin/validate/apikey"
    response = requests.post(tokenUrl, data=data, headers=auth_headers)
    return response.json()


def dataset_list():
    #TODO for now just get accountid from apikey??? or some other way
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId=accces_token["accountId"]
    accessType=accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if(accountId==None):
        return "Invalid API key"
    auth_headers = {'Authorization': 'Bearer '+accountId}
    url=serverUrl+"images/account/"+accountId+"/datasets"
    response = requests.get(url, headers=auth_headers)
    return response.json()

def createDataset(name, classname, clodustoragename):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'write' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if (name !=None and clodustoragename !=None):
        print("Started creating the dataset")
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'datasetName': name, 'cloudStorageName': clodustoragename, 'objectList': classname,'accountId':accountId}
        headers = {'Content-Type': 'application/json'}
        #print(data)
        url = serverUrl + "dataset/user/1/createfromcontainer"
        #print(url)
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        #print(response)
        #print(response.text)
        if (response.status_code == 200):
            response = "Successfully created the dataset"
        else:
            response = "Create dataset failed"
        return response

def dataset_merge(dataset_id_list, dataset_name_list,name):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'write' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if(len(dataset_id_list) >0):
        print("Started merging the datasets")
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetIdsTobeMerged': dataset_id_list,'newDatasetName':name,'accountId':accountId}
        headers = {'Content-Type': 'application/json'}

        url = serverUrl + "dataset/mergedatasets"
        response = requests.post(url, headers={"content-type":"application/json"}, data=json.dumps(data))
        if(response.status_code==200):
            response="Successfully merged the datasets"
        else:
            response="Merging failed"
        return response
    if (len(dataset_name_list) > 0):
        print("Started merging the datasets")
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'datasetNamesTobeMerged': dataset_name_list, 'newDatasetName': name, 'accountId': accountId}
        headers = {'Content-Type': 'application/json'}

        url = serverUrl + "dataset/cli/mergedatasetsbyname"
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        if (response.status_code == 200):
            response = "Successfully merged the datasets"
        else:
            response = "Merging failed"
        return response

def dataset_details(dataset_name,dataset_id):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if dataset_id != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        url=serverUrl+"dataset/cli/account/"+accountId+"/"+dataset_id
        response = requests.get(url, headers=auth_headers)
        return response.json()
    elif dataset_name != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'name': dataset_name}
        url = serverUrl + "dataset/cli/account/" + accountId
        response = requests.get(url, headers={'Content-Type': 'application/json' }, json=data)
        return response.json()

def dataset_delete(dataset_name,dataset_id):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if dataset_id != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetId': dataset_id, 'accountId': accountId}
        url = serverUrl + "dataset/cli/account/" + accountId+"/dataset/"+dataset_id+"/delete"
        response = requests.post(url, params=data)
        return response.text
    elif dataset_name != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetname': dataset_name, 'accountId': accountId}
        url = serverUrl + "dataset/cli/account/" + accountId + "/deletedatasetbyname"
        response = requests.post(url, params=data)
        return response.text

def search_details(phrase,parsedSql):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if(phrase!="None"):
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'queryphrase': phrase,'accountId':accountId,'pagenum':1}
        url = serverUrl + "search/images/1/account/"+accountId
        response = requests.post(url, params=data)
        return response.json()
    if (parsedSql != "None"):
        y = json.loads(parsedSql)
        searchRequestBody={
            "searchFilterMap": {
                "status": [],
                "dataset": []
            },
            "tagsList": []
        }
        auth_headers = {'Authorization': 'Bearer ' + accountId}
        data = {'queryphrase': y["classname"], 'accountId': accountId, 'pagenum': 1}
        url = serverUrl + "search/images/1/account/" + accountId
        response = requests.post(url, params=data,json=searchRequestBody)
        return response.json()

def containerList():
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    auth_headers = {'Authorization': 'Bearer ' + accountId}
    url = serverUrl + "cloudstorage/account/"+accountId+"/cloudlist"
    response = requests.get(url, headers=auth_headers)
    return response.json()

def createContainer(cloudstoragename,cloudtype,authentication,containername,bucketname,
            accontname,accesskey,secretid,sastoken,manifestjson,region):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    auth_headers = {'Authorization': 'Bearer ' + accountId}
    url = serverUrl + "cloudstorage/registercloud"

    if (cloudtype == "aws_s3" and authentication == "account_authentication"):
        data = { 'displayName': cloudstoragename,'provider': cloudtype,'containerName': bucketname,'authorizationType': authentication,
                'accesskey': accesskey,'secretkey': secretid,'region': region,'cloudAccountName': accontname,'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1}
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    if (cloudtype == "aws_s3" and authentication == "annonymous_access"):
        data = {'displayName': cloudstoragename,
                'provider': cloudtype,
                'containerName': bucketname,
                'authorizationType': authentication,
                'accesskey': accesskey,
                'secretkey': secretid,
                'region': region,
                'cloudAccountName': accontname,
                'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1
                }
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    if (cloudtype == "azure_container" and authentication == "account_authentication"):
        data = {'displayName': cloudstoragename,
                'provider': cloudtype,
                'containerName': containername,
                'authorizationType': authentication,
                'accesskey': accesskey,
                'secretkey': secretid,
                'region': region,
                'cloudAccountName': accontname,
                'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1
                }
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    if (cloudtype == "azure_container" and authentication == "annonymous_access"):
        data = {'displayName': cloudstoragename,
                'provider': cloudtype,
                'containerName': containername,
                'authorizationType': authentication,
                'accesskey': accesskey,
                'secretkey': secretid,
                'region': region,
                'cloudAccountName': accontname,
                'sasToken': sastoken,
                'accountId': accountId,
                'jsonFileNmae': manifestjson,
                'status': 1
                }
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text

def container_details(cloudstoragename,cloudstorageid):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if cloudstorageid != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        url=serverUrl+"cloudstorage/account/"+accountId+"/cloudstoragedetailsbyid/"+cloudstorageid
        response = requests.get(url, headers=auth_headers)
        return json.dumps(response.json(), indent=3)
    elif cloudstoragename != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'storagename': cloudstoragename}
        url=serverUrl+"cloudstorage/account/"+accountId+"/cloudstoragedetailsbyname"
        response = requests.get(url,params=data)
        return response.text

def delete_container(cloudstorage_name,cloudstorage_id):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if cloudstorage_id != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetId': cloudstorage_id, 'accountId': accountId}
        url = serverUrl + "cloudstorage/account/" + accountId+"/cloudstorage/"+cloudstorage_id+"/delete"
        response = requests.post(url, params=data)
        return response.text
    elif cloudstorage_name != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {'datasetname': cloudstorage_name, 'accountId': accountId}
        url = serverUrl + "cloudstorage/account/" + accountId + "/cloudstorage/deletecloudstoragebyname"
        response = requests.post(url, params=data)
        return response.text


def nosqlreslt(phrase):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if (phrase != "None"):
        queryRequestBody={"tables":None,
        "selectColumns":None,
        "whereClause":None,
        "mongoDbNativeQuery":str(phrase),
        "queryOtherComponents":None
        }
        #print(queryRequestBody)
        url = serverUrl + "query/1/account/" + accountId
        response=""
        response = requests.post(url,json=queryRequestBody)
        return response.json()


def sqlreslt(parsedData):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if (parsedData != "None"):
        table=parsedData[0]
        column=parsedData[1]
        whereClause=parsedData[2]
        limit=parsedData[3]
        whereClauselist = json.loads(whereClause)
        whereclause={}
        for key in whereClauselist:
            value = whereClauselist[key]
            x=str(value).replace('"', '')
            if(key=="active" or key=="status" or key=="annotated" or key=="approved" or key=="redo" or key=="excludeFromAnnotation"):
                 whereclause[key]=int(x)
            else:
                whereclause[key] = x
        if(len(column)==0):
            column=None
        if (len(whereclause) == 0):
            whereclause = None
        queryRequestBody = {'tables': [table],
                            'selectColumns': column,
                            'limit': int(limit),
                            'whereClause': whereclause,
                            'mongoDbNativeQuery': None,
                            'queryOtherComponents': None
                            }
        #print(queryRequestBody)
        url = serverUrl + "query/1/account/" + accountId
        #print(url)
        response = ""
        response = requests.post(url, json=queryRequestBody)
        #print(response.status_code)
        return response.json()

def dataset_download(datasetid,datasetname, filters_list,format):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'write' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    print("Started downloading the datasets")
    auth_headers = {'Authorization': 'Bearer ' + accountId}
    if (len(filters_list) == 0):
        filters_list = ""
    data = {'datasetId': datasetid, 'datasetname': datasetname, 'filters': filters_list, 'format': format}
    auth_headers = {'Authorization': 'Bearer ' + accountId}
    url = serverUrl + "admin/account/1/downloaddataset"
    response = requests.post(url, data=data, headers=auth_headers)
    if (response.status_code == 200):
        response = response.json()
        transactionId = response['transactionId']
        status = response['status']
        if (status == 0):
            print("Downloading please wait ...")
            while (True):
                url = serverUrl + "admin/account/" + accountId + "/downloadtrain/id/" + transactionId + "/status"
                response = requests.post(url)
                response = response.json()
                downloadstatus = response['status']
                if (downloadstatus == 0):
                    time.sleep(5)
                elif (downloadstatus == -1):
                    print("Download failed. Please retry")
                elif (downloadstatus == 1):
                    print(response['progress'])
                    downloadUrl = response['downloadUrl']
                    wget.download(downloadUrl)
                    break

def assign_dataset(email, datasets):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if(email !=None):
        if(len(datasets)!=0):
            auth_headers = {'Authorization': 'Bearer '+accountId}
            data = {'email' :email,'accessibleDatasetIds':datasets}
            url = serverUrl + "admin/assigndataset"
            response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
            if (response.status_code == 200):
                response = "Successfully assigned the datasets"
            else:
                response = "Dataset assign failed"
            return response
        else:
            return "Invalid please provide valid details"
    else:
        return "Invalid please provide valid details"
 
def delete_user(users):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if(len(users)!=0):
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = { 'email' :users}
        url = serverUrl + "admin/deleteuser"
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    else:
        return "Invalid please provide valid details"


def get_users():
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    auth_headers = {'Authorization': 'Bearer '+accountId}
    url = serverUrl + "admin/account/"+accountId+"/getusers"
    response = requests.get(url)
    return json.dumps(response.json(), indent=3)

def edit_user(email,role):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if email != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = { 'email' :email,'role':role,'accountId':accountId}
        url = serverUrl + "admin/edituser"
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    else:
        return "Invalid please provide valid details"

def add_user(name, email,password,role):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if email != "None":
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = { 'email' :email,'password' :password,'name':name,'role':role,'accountId':accountId}
        url = serverUrl + "admin/adduser"
        response = requests.post(url, headers={"content-type": "application/json"}, data=json.dumps(data))
        return response.text
    else:
        return "Invalid please provide valid details"

def processCvfunctions(operation,cvargs,datasetname,datasetid):
    accces_token = generate_access_token_from_apikey()
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'read' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if (datasetname != "" or datasetid !=""):

        cvfnctioninfo = { 'datasetId': datasetid,
                          'datasetName': datasetname,
                          'cvargs':cvargs,
                          'operation':operation
                        }
        #print(cvfnctioninfo)
        url = serverUrl + "trainset/account/" + accountId+"/getcvfnctioninfo"
        response = ""
        opType="default"
        if(len(operation)>0):
            tmp=operation[0]
            if(tmp=="copy"):
                opType="copy"
            elif(tmp=="download"):
                opType="download"
        if(opType=="default" or opType=="copy"):
            response = requests.post(url, json=cvfnctioninfo)
            print(response.text)
        elif(opType=="download"):
            response = requests.post(url, json=cvfnctioninfo)
            print("Getting the data please wait ...")
            msg=response.text
            #print(msg)
            outdata=msg.split("||")
            object_name=outdata[0]
            accessKey=outdata[1]
            secret=outdata[2]
            bucket = "polygon-download"
            n=5;

            while n > 0:
                sesssion = boto3.Session(accessKey, secret)
                s3 = sesssion.client('s3')
                obj_status = s3.list_objects(Bucket=bucket, Prefix=object_name)
                if obj_status.get('Contents'):
                    s3_url = s3.generate_presigned_url(
                        ClientMethod='get_object',
                        Params={'Bucket': bucket, 'Key': object_name, },
                        ExpiresIn=100000,
                    )
                    print("Downloading please wait ...")
                    home = str(Path.home())
                    wget.download(s3_url,out=home)
                    print("\n Successfully downloaded the file to " + str(home)+"/"+object_name)
                    n=0
                else:
                    time.sleep(10)

def dataset_version(datasetid, datasetname,filters_list,name):
    accces_token = generate_access_token_from_apikey()
    #print(accces_token)
    if (accces_token == "Not Found" or accces_token == "Not Found"):
        return "API KEY not Found, Please run 'polygon --configure' to configure"
    accountId = accces_token["accountId"]
    accessType = accces_token["accessList"]
    if not 'write' in accessType:
        return "API does not have the read access"
    if (accountId == None):
        return "Invalid API key"
    if(datasetid!=""):
        auth_headers = {'Authorization': 'Bearer '+accountId}
        data = {"parentDatasetId": datasetid,'augmentationType': filters_list,'versionName':name,"provider": "polygonCloud",'accountId':accountId}
        headers = {'Content-Type': 'application/json'}

        url = serverUrl + "trainset/user/1/account/"+accountId+"/createversion"
        response = requests.post(url, headers={"content-type":"application/json"}, data=json.dumps(data))
        if(response.status_code==200):
            response="Successfully created  the version"
        else:
            response="Create version failed"
        return response