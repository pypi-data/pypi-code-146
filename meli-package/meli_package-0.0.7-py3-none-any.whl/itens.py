import requests as rq

global_url = 'https://api.mercadolibre.com'

def itemSearchCategory(access_token, site_id, category_id):
    r'''
        Obter itens listados numa categoria.
    '''
    url = f'{global_url}/sites/{site_id}/search?category={category_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemKeywordSearch(access_token, site_id, keywords):
    r'''
        Obter itens de uma consulta de busca.  
    '''
    url = f'{global_url}/sites/{site_id}/search?q={keywords}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemNicknameSearch(access_token, site_id, nickname):
    r'''
        Obter itens das listagens por nickname.
    '''
    url = f'{global_url}/sites/{site_id}/search?nickname={nickname}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemSellerIdSearch(access_token, site_id, seller_id):
    r'''
        Permite listar itens por vendedor.
    '''
    url = f'{global_url}/sites/{site_id}/search?seller_id={seller_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemSellerIdCategorySearch(access_token, site_id, seller_id, category_id):
    r'''
        Obter itens das listagens por vendedor numa categoria específica.  
    '''
    url = f'{global_url}/sites/{site_id}/search?seller_id={seller_id}&category={category_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.post(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemUserIdSearch(access_token, user_id):
    r'''
        Permite listar todos os itens da conta de um vendedor.    
    '''
    url = f'{global_url}/users/{user_id}/items/search'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemMultiget(access_token, itens):
    r'''
        Multiget com múltiplos números de itens.  
    '''
    url = f'{global_url}/items/?ids='
    for item in itens:
        url += f'{item[0]},'
    url = url[:-1]
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemUserMultiget(access_token, users):
    r'''
        Multiget com múltiplos números de usário.  
    '''
    url = f'{global_url}/items/?users='
    for user in users:
        url += f'{user[0]},'
    url = url[:-1]
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemSearchScan(access_token, user_id, scroll_id=None):
    r'''
        Permite obter mais de 1000 itens
         correspondentes a um usuário.
    '''
    if scroll_id is not None:
        url = f'{global_url}/users/{user_id}/items/search?search_type=scan&scroll_id={scroll_id}'
        header = {
            'Content-type': 'Application/JSON',
            'Authorization': f'Bearer {access_token}' 
        }
        data = rq.get(url, headers=header)
        dataJson = data.json()
        data.close()
        return dataJson

    url = f'{global_url}/users/{user_id}/items/search?search_type=scan'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}' 
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson
