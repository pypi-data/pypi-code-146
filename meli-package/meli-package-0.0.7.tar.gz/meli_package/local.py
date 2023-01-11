import requests as rq

global_url = 'https://api.mercadolibre.com'

def classifiedLocation(access_token):
    r'''
        Obtém informação de países.
    '''
    url = f'{global_url}/classified_locations/countries'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def countryInfo(access_token, country_id):
    r'''
        Obtém informação de países by country_id.  
    '''
    url = f'{global_url}/classified_locations/countries/{country_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def stateInfo(access_token, state_id):
    r'''
        Obtém estado da informação.
    '''
    url = f'{global_url}/classified_locations/states/{state_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def cityInfo(access_token, city_id):
    r'''
        Obtém estado da informação da cidade.   
    '''
    url = f'{global_url}/classified_locations/cities/{city_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def zipCodeInfo(access_token, country_id, zip_code):
    r'''
        Recupera dados da localização por código postal.  
    '''
    url = f'{global_url}/countries/{country_id}/zip_codes/{zip_code}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def zipCodeSearchBetween(access_token, country_id, zip_code_from, zip_code_to):
        r'''
            Obtém todos os códigos postais para um country_id entre dois valores dados.   
        '''
        url = f'{global_url}/country/{country_id}/zip_codes/search_between?zip_code_from={zip_code_from}&zip_code_to={zip_code_to}'
        header = {
            'Content-type': 'Application/JSON',
            'Authorization': f'Bearer {access_token}'
        }
        data = rq.get(url, headers=header)
        dataJson = data.json()
        data.close()
        return dataJson


