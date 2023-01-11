import requests as rq

global_url = 'https://api.mercadolibre.com/'


def userMe(access_token):
    r'''
        Informação da conta do usuário.
    '''
    url = f'{global_url}users/me'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    user_data = rq.get(url, headers=header)
    dataJson = user_data.json()
    user_data.close()
    return dataJson


def user(access_token, user_id):
    r'''
        Obtém a informação do usuário que fez login na conta.
    '''
    url = f'{global_url}users/{user_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def userAddress(access_token, user_id):
    r'''
        Obtém endereços associados à conta do usuário.
    '''
    url = f'{global_url}users/{user_id}/addresses'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer f{access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def userPaymentMethods(access_token, user_id):
    r'''
        Obtém os métodos de pagamento aceitos pelo vendedor para cobrar.
    '''
    url = f'{global_url}users/{user_id}/accepted_payment_methods'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def Application(access_token, application_id):
    r'''
        Obtém dados sobre o aplicativo.
    '''
    url = f'{global_url}/applications/{application_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def userBrands(access_token, user_id):
    r'''
        Este processo recupera marcas associadas a um user_id. O atributo oficial_store identifica uma loja.
    '''
    url = f'{global_url}users/{user_id}/brands'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def classifiedPromotionPacks(access_token, user_id, listing_type=False, category_id=False):
    r'''
        Este processo recupera marcas associadas a um user_id. O atributo oficial_store identifica uma loja.
    '''
    url = f'{global_url}users/{user_id}/classifieds_promotion_packs'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization' : f'Bearer {access_token}'
    }

    if listing_type and category_id:
        url += f'/{listing_type}&CATEGORYID={category_id}'

    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson

def availableListingTypes(access_token, user_id, category_id):
    r'''
        Listing types disponivéis por usuários e categorias.
    '''
    url = f'{global_url}users/{user_id}/available_listing_types?category_id={category_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }

    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def listingTypesByID(access_token, user_id, listing_type_id, category_id):
    r'''
        Obter o listing types disponível por um tipo de listagem segundo uma categoria outorgada.
    '''
    url = f'{global_url}users/{user_id}/available_listing_type/{listing_type_id}?category_id={category_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def ApplicationPermissions(access_token, user_id, application_id):
    r'''
        Permissão do aplicativo.
    '''
    url = f'{global_url}users/{user_id}/applications/{application_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def myFeedApp(access_token, application_id):
    r'''
        Histórico de notificações
    '''
    url = f'{global_url}myfeeds?app_id={application_id}'
    header = {
        'Content-type': 'ApplicationJSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson