import requests as rq

global_url = 'https://api.mercadolibre.com'


def sellerOrders(access_token, seller_id):
    r'''
        Buscar os pedidos de um vendedor
    '''
    url = f'{global_url}/orders/search?seller={seller_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def orderInfo(access_token, seller_id, order_id):
    r'''
        Buscar um pedido de um vendedor
    '''
    url = f'{global_url}/orders/search?seller={seller_id}&q={order_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def buyerOrders(access_token, buyer_id):
    r'''
        Buscar os pedidos de um comprador
    '''
    url = f'{global_url}/orders/search?buyer={buyer_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Beare {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def paymentInfo(access_token, payment_id):
    r'''
        Obter dados do pagamento segundo o perfil do pagador
    '''
    url = f'https://api.mercadopago.com/v1/payments/{payment_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def paymentMethods(access_token, site_id):
    r'''
        Retorna os métodos de pagamentos previstos pelo Mercado Pago
    '''
    url = f'{global_url}/sites/{site_id}/payment_method'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}' 
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def paymentMethodDetail(access_token, site_id, payment_method_id):
    r'''
        Retorna os dados de um método de pagament específico
    '''
    url = f'{global_url}/sites/{site_id}/payment_methods/{payment_method_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def orderFeedback(access_token, order_id):
    r'''
        Obter feedbacks de um comprador ou vendedor de um pedido
    '''
    url = f'{global_url}/orders/{order_id}/feedback'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def orderBlacklist(access_token, seller_id):
    r'''
        Obter os usuários bloqueados por oferta nos items de um vendedor
    '''
    url = f'{global_url}/users/{seller_id}/order_blacklist'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def orderProducts(access_token, order_id):
    r'''
        Obter os dados do produto vendido no pedido
    '''
    url = f'{global_url}/orders/{order_id}/product'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


