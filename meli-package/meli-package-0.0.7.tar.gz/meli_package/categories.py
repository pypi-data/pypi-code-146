import requests as rq



global_url = 'https://api.mercadolibre.com'

def category(access_token, category_id):
    r'''
        Devolve informação sobre a categoria.
    '''
    url = f'{global_url}/categories/{category_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def categoriesAttributes(access_token, category_id):
    r'''
        Mostra os atributos e regulas com a finalidade de descrever os elementos que se guardam em cada categoria.
    '''
    url = f'{global_url}/categories/{category_id}/attributes'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def classifiedPromotionPacks(access_token, category_id):
    r'''
        Obtém packs de promoções classificadas por categorias.
    '''
    url = f'{global_url}/categories/{category_id}/classifieds_promotion_packs'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson