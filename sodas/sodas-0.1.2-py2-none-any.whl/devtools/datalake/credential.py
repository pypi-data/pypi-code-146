import json
import requests

def _get_credential_object_storage(
        base_url: str, 
        access_token: str, 
        end_point: str
    ):
    
    optionGetObjectStorageCredental = {
        'url': 'http://' + base_url + '/api/v1/data-lake/object-storage/credential/list',
        'params': {
            'offset': 0,
            'limit': 10
        },
        'headers': {
            'Authorization': 'Bearer ' + access_token
        }
    }
    try :
        res = requests.get(optionGetObjectStorageCredental['url'],
                    headers=optionGetObjectStorageCredental['headers'],
                    params=optionGetObjectStorageCredental['params'])

        if res.status_code != 200:
            raise Exception(res.status_code)
        else :
            res = res.json()
            return res
            
    except Exception as e:
        print(e)


def _get_credential_key(response: json):
    # 일단 한개만 있다고 가정함
    access_key = response['results'][0]['accessKey']
    secret_key = response['results'][0]['secretKey']
    
    return access_key, secret_key

    