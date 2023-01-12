import os
import requests
import numpy as np
import json

def get_access_token(creds):
    
    creds['client_id'] = os.environ['CODA_NOTEBOOK_APP_AUTH_CLIENT_ID']
    creds['client_secret'] = os.environ['CODA_NOTEBOOK_APP_AUTH_CLIENT_SECRET']
    creds['grant_type'] = 'password'
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    auth_response = requests.post(os.environ['CODA_AUTH_SERVICE_URL'] + '/realms/' + os.environ['CODA_NOTEBOOK_APP_AUTH_REALM'] + '/protocol/openid-connect/token', data=creds,headers=headers)
    return json.loads(auth_response.text)['access_token']

def execute_query(service, action, sites, query, access_token):
    
    headers = {'Authorization': 'Bearer ' + access_token }
    data_response = requests.get(os.environ['CODA_HUB_API_URL'] + 
      '/' + service + '/' + action + '?sites=' + (','.join(sites)), 
                                 json=query,headers=headers)

    data = json.loads(data_response.text)

    return data

def get_measure(data, measure):
    vals = np.asarray([[[z[measure] for z in x['results']] for x in y] for y in data]).flatten()
    keys = np.asarray([[x['siteCode'] for x in y] for y in data]).flatten()
    return dict(zip(keys,vals))