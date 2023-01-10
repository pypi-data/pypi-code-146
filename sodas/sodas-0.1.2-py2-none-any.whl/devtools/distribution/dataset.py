import json
import requests

def _get_dataset_list(base_url: str, access_token: str) :
    optionsGetDatasetList = {
        'url': 'http://' + base_url + '/api/v1/data-management/dataset/list',
        'headers': {
            'accept' : 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
    }
    try:
        res = requests.get(optionsGetDatasetList['url'],
                        headers=optionsGetDatasetList['headers'],
                        )
        if res.status_code == 200:
            res = res.json()
            return res
        else :  
            raise Exception('Unauthorized. Cannot access API.')
    except Exception as e:
        print(e)

def _find_dataset_id(response: json):
    # 일단 dataset이 한개만 있다고 가정하고 작성
    return response['results'][0]['id']
