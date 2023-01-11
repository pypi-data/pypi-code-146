import requests as rq

global_url = 'https://api.mercadolibre.com/'


def currencies(access_token):
    r'''
       	Obtém estado da informação sobre todas as moedas disponíveis no Mercado Livre.     
    '''
    url = f'{global_url}/currencies'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def currencyInfo(access_token, currency_id):
    r'''
        Obtém informação sobre as moedas disponíveis no Mercado Livre por currency_id.
    '''
    url = f'{global_url}/currencies/{currency_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def currencyConversion(access_token, currency_from, currency_to):
    r'''
        Recupera a conversão das moedas que Mercado Livre utiliza nos cálculos.
    '''
    url = f'{global_url}/currency_conversions/search?from={currency_from}&to={currency_to}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson



