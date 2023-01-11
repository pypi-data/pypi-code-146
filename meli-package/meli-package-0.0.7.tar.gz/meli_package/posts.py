import requests as rq

global_url = 'https://api.mercadolibre.com'



def sites(access_token):
    r'''
        Devolve informação sobre os sites onde o Mercado Livre está disponível.
    '''
    url = f'{global_url}/sites'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def siteDomains(access_token, site_domain_url):
    r'''
        Devolve informação sobre o domínio.
    '''
    url = f'{global_url}/site_domains/{site_domain_url}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def siteListingTypes(access_token, site_id):
    r'''
        Devolve informação sobre o listing types.
    '''
    url = f'{global_url}/sites/{site_id}/listing_types'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def listingExposures(access_token, site_id):
    r'''
        Devolve diferentes níveis de exposição associados com todos os listing_types no Mercado Livre.
    '''
    url = f'{global_url}/sites/{site_id}/listing_exposures'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def listingPrices(access_token, site_id, price):
    r'''
        Devolve a listagem de preços para vender e comprar no Mercado Livre.
    '''
    url = f'{global_url}/sites/{site_id}/listing_prices?price={price}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }

    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def listingCategories(access_token, site_id):
    r'''
    	Devolve as categorias disponíveis no site.
    '''
    url = f'{global_url}/sites/{site_id}/categories'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def domainDiscovery(access_token, site_id, q):
    r''' 
        Preditor de categorias. Devolve a categoria e domínio correspondentes para enquadrar um anúncio baseado no título, domínio e atributos
    '''
    url = f'{global_url}/sites/{site_id}/domain_discovery/search?q={q}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def listingTypeConfig(access_token, site_id, listing_type_id):
    r'''
        Obtém a configuração especifica de listing_type.  
    '''
    url = f'{global_url}/sites/{site_id}/listing_types/{listing_type_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson