import requests as rq

global_url = 'https://api.mercadolibre.com'


def intervalDateUserVisit(access_token, user_id, date_from, date_to):
    r'''
        Obtem as visitas que um usuário teve em um intervalo de tempo
    '''
    url = f'{global_url}/users/{user_id}/item_visits?date_from={date_from}&date_to={date_to}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def timeWindowVisits(access_token, user_id, last, unit, ending):
    r'''
        Devolve as visitas de um usuário em cada item publicado durante um período de tempo. O detalhe da informação é agrupado por intervalos de tempo
    '''
    url = f'{global_url}/users/{user_id}/items_visits/timewindow?last={last}&unit={unit}&ending={ending}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def intervalContactQuestion(access_token, user_id, date_from, date_to):
    r'''
        Devolve o total de perguntas de um usuário específico em todos os items publicados num intervalo de datas.
    '''
    url = f'{global_url}/users/{user_id}/contacts/questions?date_from={date_from}&date_to={date_to}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def timeWindowContactQuestions(access_token, user_id, last, unit):
    r'''
        O recurso permite obter as perguntas realizadas num determinado tempo nos items publicados por um seller. 
    '''
    url = f'{global_url}/users/{user_id}/contacts/questions/time_window?last={last}&unit={unit}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def intervalPhoneViews(access_token, user_id, date_from, date_to):
    r'''
        Pode obter a quantidade de vezes que fizeram clique em "Ver telefone" dentro de um item durante um período de tempo.
    '''
    url = f'{global_url}/users/{user_id}/contacts/phone_views?date_from={date_from}&date_to={date_to}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authentication': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def timeWindowPhoneViews(access_token, user_id, last, unit):
    r'''
        Devolve a quantidade de vezes que foi clicado na opção “ver telefone” para cada item de um usuário num intervalo de datas.
    '''
    url = f'{global_url}/users/{user_id}/contacts/phone_view/time_window?last={last}&unit={unit}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def timeWindowItemView(access_token, item_id, last, unit, ending):
    r'''
        Devolve as visitas de um item num intervalo de tempo, filtrando por unidade e parâmetro de finalização.  
    '''
    url = f'{global_url}/items/{item_id}/visits/time_window?last={last}&unit={unit}&ending={ending}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson
