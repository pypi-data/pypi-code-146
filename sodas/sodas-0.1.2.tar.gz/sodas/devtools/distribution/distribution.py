import os
import json

import requests

def _get_distribution_list(
    base_url: str, 
    access_token:str, 
    dataset_id: str
    ):
    
    optionsGetDistributionList = {
        'url': 'http://' + base_url + '/api/v1/data-management/distribution/list',
        'params': {
            'datasetId': dataset_id,
        },
        'headers': {
            'accept' : 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
    }
    
    try:
        res = requests.get(optionsGetDistributionList['url'],
                        headers=optionsGetDistributionList['headers'],
                        params=optionsGetDistributionList['params'])

        if res.status_code == 200:
            res = res.json()
            return res
        else :
            raise Exception(res.status_code, res.content)
    except Exception as e:
        print(e)

def _find_distribution_id(response: json, file_name: str):
    results = response['results']
    for result in results:
        if(file_name == result['fileName']):
            return result['id']

def _get_distribution (base_url: str, access_token: str, distribution_id: str):
    optionsGetDistribution = {
        'url': 'http://' + base_url + '/api/v1/data-management/distribution/get',
        'params': {
            'id': distribution_id
        },
        'headers': {
            'accept' : 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
    }
    
    try:
        res = requests.get(optionsGetDistribution['url'],
                        headers=optionsGetDistribution['headers'],
                        params=optionsGetDistribution['params'])
        
        if res.status_code == 200:
            distribution = json.loads(res.content.decode('ascii'))
            return distribution
        else :
            raise Exception(res.status_code, res.content)
    except Exception as e:
        print(e)

def _find_file_name(response: json):
    return response['id'] + '.' + response['fileName'].split('.').pop()

def _find_bucket_name(response: json):
    return response['issuerId'].replace('_', '')
