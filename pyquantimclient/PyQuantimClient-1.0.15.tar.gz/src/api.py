# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests, json

class quantim:
    def __init__(self, username, password, secretpool, env="qa"):
        self.username = username
        self.password = password
        self.secretpool = secretpool
        self.env = env

    def get_header(self):
        if self.secretpool=='ALM':
            token_url = "https://api-quantimqa.sura-im.com/oauthback/token" if self.env=="qa" else "https://api-quantim.sura-im.com/oauthback/token"
            data = {"username":self.username, "password":self.password}
        else:
            token_url = "https://api-quantimqa.sura-im.com/tokendynamicpool" if self.env=="qa" else "https://api-quantim.sura-im.com/tokendynamicpool"
            data = {"username":self.username, "password":self.password, "secretpool":self.secretpool}

        headers = {"Accept": "*/*",'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        access_token_response = requests.post(token_url, data=json.dumps(data), headers=headers, verify=False, allow_redirects=False)
        tokens = json.loads(access_token_response.text)
        access_token = tokens['id_token']
        api_call_headers = {"Accept": "*/*", 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

        return api_call_headers

    def api_call(self, endpoint, method="post", data=None, verify=False):
        '''
        data: when method get, data is an array of key values.
        '''
        api_call_headers = self.get_header()
        if method.lower()=='post':
            api_url = f"{'https://api-quantimqa.sura-im.com/' if self.env=='qa' else 'https://api-quantim.sura-im.com/'}{endpoint}"
            api_call_response = requests.post(api_url, headers=api_call_headers, data=json.dumps(data), verify=verify)
        elif method.lower()=='get':
            api_url = f"{'https://api-quantimqa.sura-im.com/' if self.env=='qa' else 'https://api-quantim.sura-im.com/'}{endpoint}"
            if data is not None:
                api_url = api_url + '?'+'&'.join([f"{x['key']}={x['value']}" for x in data])
            api_call_response = requests.get(api_url, headers=api_call_headers, data=None, verify=verify)
        else:
            print("Method not supported!")
            return None
        return json.loads(api_call_response.text)

    def retrieve_s3_df(self, bucket, key, sep=','):
        '''
        Get series
        '''
        data = {'bucket':bucket, 'key':key, 'sep':sep}
        resp = self.api_call('retrieve_data_s3', method="post", data=data, verify=False)
        df = pd.DataFrame(resp)
        return df

    def load_s3_df(self, df, bucket, key, sep=',', overwrite=True):
        '''
        Load file to s3.
        '''
        payload = df.to_dict(orient='records')
        data = {'bucket':bucket, 'file_name':key, 'payload':payload, 'sep':sep, 'overwrite':overwrite}
        try:
            resp = self.api_call('load_data_s3', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}
        return resp
