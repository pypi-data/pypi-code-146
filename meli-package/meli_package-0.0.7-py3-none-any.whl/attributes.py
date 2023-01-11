import requests as rq

global_url = 'https://api.mercadolibre.com'


def categoriesAttributes(access_token, category_id):
    r'''
        Consultar atributos relacionados a categoria
    '''
    url = f'{global_url}/categories/{category_id}/attributes'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def technicalSpecsInput(access_token, category_id):
    r'''
        Obter os atributos obrigatórios de cada categoria
    '''
    url = f'{global_url}/categories/{category_id}/technical_specs/input'
    header = {
        'Content-Type': 'Application/JSON', 
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def technicalSpecsOutput(access_token, category_id):
    r'''
        Mostrar os seus produtos e como vão ser visualizados
    '''
    url = f'{global_url}/categories/{category_id}/technical_specs/output'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def conditionalAttributes(access_token, catergory_id):
    r'''
        Consultar se os atributos que tem a tag 'conditional_required' são necessários para sua publicação
    '''
    url = f'{global_url}/categories/{catergory_id}/attributes/conditional'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def incompleteTechnicalSpecs(access_token, user_id):
    r'''
        Produtos que foram penalizados com a tag 'incomplete_technical_specs'
    '''
    url = f'{global_url}/users/{user_id}/items/search?tags=incomplete_technical_specs'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson

def notApplicableAttribute(access_token, item_id):
    r'''
        Especificar atributos que não se aplicam a determinado item
    '''
    url = f'{global_url}/items/{item_id}?attributes=attributes&include_internal_attributes=true'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson
