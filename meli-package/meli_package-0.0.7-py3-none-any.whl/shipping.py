import requests as rq

global_url = 'https://api.mercadolibre.com'


def shipmentInfo(access_token, shipment_id):
    r'''
        Devolve todos os dados do envio.
    '''
    url = f'{global_url}/shipments/{shipment_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def itemShippingOption(access_token, item_id):
    r'''
        Devolve todos os métodos disponíveis para fazer o envio de um produto. Válido somente para envios custom.  
    '''
    url = f'{global_url}/item/{item_id}/shipping_options'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def siteShipmentMethods(access_token, site_id):
    r'''
        Devolve os métodos de entrega disponíveis num país.
    '''
    url = f'{global_url}/sites/{site_id}/shipping_methods'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def catergoryShipment(access_token, cust_id, category_id):
    r'''
        Devolve os métodos de envio disponíveis para determinada categoria
    '''
    url = f'{global_url}/users/{cust_id}/shipping_modes?category_id={category_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def userShippingPreferences(access_token, cust_id):
    r'''
        Devolve todos os modos de envio e serviços disponíveis para o usuário.     
    '''
    url = f'{global_url}/users/{cust_id}/shipping_preferences'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def orderShipments(access_token, order_id):
    r'''
        Devolve as informações de envio dentro da order. 
    '''
    url = f'{global_url}/orders/{order_id}/shipments'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def shipmentLabels(access_token, shipment_id):
    r'''
        Permite imprimir a etiqueta para enviar o pedido
    '''
    url = f'{global_url}/shipment_labels?shipment_id={shipment_id}'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def printShipmentLabelZPL(access_token, shipment_id):
    r'''
        Permite imprimir a etiqueta em formato Zebra para enviar o pedido.
    '''
    url = f'{global_url}/shipment_labels?shipment_id={shipment_id}&response_type=zpl2'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson


def printShipmentPDF(access_token, shipment_id):
    r'''
        Permite imprimir a etiqueta em formato PDF para enviar o pedido.
    '''
    url = f'{global_url}/shipment_labels?shipment_id={shipment_id}&savePDF=Y'
    header = {
        'Content-Type': 'Application/JSON',
        'Authorization': f'Bearer {access_token}'
    }
    data = rq.get(url, headers=header)
    dataJson = data.json()
    data.close()
    return dataJson