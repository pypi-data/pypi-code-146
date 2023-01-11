import requests as rq
import environs
import webbrowser as web
import sys

def authentication(code=False, refresh_token=False):
    env = environs.Env()
    environs.Env.read_env()
    if refresh_token:
        refresh_url = "https://api.mercadolibre.com/oauth/token"
        header = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'client_id': env('CLIENT_ID'),
            'client_secret': env('CLIENT_SECRET'),
            'refresh_token': refresh_token
        }
        access = rq.post(refresh_url, headers=header, data=data)
        accessJson = access.json()
        access.close()
        return accessJson

    if code:
        code_url = "https://api.mercadolibre.com/oauth/token"
        header = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'client_id': env('CLIENT_ID'),
            'client_secret': env('CLIENT_SECRET'),
            'code': f'{code}',
            'redirect_uri': env('REDIRECT_URI')
        }
        access = rq.post(code_url, headers=header, data=data)
        accessJson = access.json()
        access.close()
        return accessJson
    else:
        return 'Give at least one argument'
        