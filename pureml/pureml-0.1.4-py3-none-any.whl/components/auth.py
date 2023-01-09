
from pureml.utils.constants import BASE_URL
from urllib.parse import urljoin
import requests
import json
from rich import print
from pureml.cli.auth import save_auth
from . import get_org_id, get_token

def login(org_id:str, access_token:str) -> str:
    ''' The function takes in a user API token and logs in a user for a session.
    
    Parameters
    ----------
    token: str
        API token for the user. This token will be used to authenticate an user.
    
    '''
    
    url_path_1 = 'org/id/{}'.format(org_id)
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }


    response = requests.get(url, headers=headers)

    # print(response.text)
    if response.status_code == 200:

        response_text = response.text
        response_org_details = json.loads(response_text)['data']
        
        # if response_org_details is not None:
        response_org_id = response_org_details[0]['id']

        if response_org_id == org_id:
            print('[green] Valid Org Id and Access token')
            save_auth(org_id=org_id, access_token=access_token)
        
        else:
            print('[orange] Valid Org Id and Access token. Obtained different organization')

        # else:
        #     print('[green] Invalid Org Id and Access token')
    elif response.status_code == 403:
        print('[red] Invalid Access token')
    elif response.staus_code == 404:
        print('[red] Invalid Org Id')
    else:
        print("[red] Unable to obtain the organization details")



    
def details():
    token = get_token()
    org_id = get_org_id()

    print('Org Id: ', org_id)
    print('Access Token: ', token)        

