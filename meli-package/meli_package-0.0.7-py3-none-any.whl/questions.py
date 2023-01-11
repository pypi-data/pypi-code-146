import requests as rq

global_url = 'https://api.mercadolibre.com'


def questionItem(access_token, item_id):
    r'''
        Busca uma pergunta feita nos items do usuário
    '''
    url = f'{global_url}/questions/search?item={item_id}'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def doQuestion(access_token, item_id, question_text):
    r'''
        Fazer perguntas sobre os items de outros usuários.
    '''
    url = f'{global_url}/questions'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    body = {
        'text': f'{question_text}',
        'item_id': f'{item_id}'
    }
    data = rq.post(url, headers=header, data=body)
    dataJson = data.json()
    data.close()
    return dataJson


def doAnswer(access_token, question_id, answer_text):
    r'''
    	Responder às perguntas realizadas em seus items.
    '''
    url = f'{global_url}/answers'
    header = {
        'Content-type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    body = {
        'question_id': f'{question_id}',
        'text': f'{answer_text}'
    }
    data = rq.post(url, headers=header, data=body)
    dataJson = data.json()
    data.close()
    return dataJson

def getQuestion(access_token, question_id):
    r'''
        Obter informação de uma pergunta especifica de um ID.
    '''
    url = f'{global_url}/questions/{question_id}'
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def questionsBlacklist(access_token, seller_id, buyer_id):
    r'''
    	Gerenciar perguntas da blacklist.
    '''
    url = f'{global_url}/users/{seller_id}/questions_blacklist/{buyer_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def blockUser(access_token, seller_id, user_id):
    r'''
        Inserir usuário na blacklist
    '''
    url = f'{global_url}/users/{seller_id}/questions_blacklist'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    body = {
        'user_id': user_id
    }
    data = rq.post(url, headers=header, data=body)
    dataJson = data.json()
    data.close()
    return dataJson


def deleteBlockedUser(access_token, seller_id, user_id):
    r'''
        Remover um usuário bloqueado
    '''
    url = f'{global_url}/users/{seller_id}/questions_blacklist/{user_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.delete(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def receivedQuestion(access_token):
    r'''
        Perguntas recebidas por usuário.
    '''
    url = f'{global_url}/my/received_questions/search'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson