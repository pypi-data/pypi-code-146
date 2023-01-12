import typing

import mercadopago
from bson import ObjectId
from dateutil.relativedelta import *

from .dates import (calculate_payment_date, get_periodo, set_next_vigency,
                    today_argentina)
from .format import datetime_parser
from .init_creds import init_mongo
from .payments import (create_payment_data, get_card_data_from_payment, get_cards, get_client_price,
                       get_empty_card, update_payment_data)

db = init_mongo()


def member_unsubscribe(member: dict, reason, source, unsubscribe_request=False, status_boleta_inactivado='expired'):
    """ Da de baja un socio modificando los parámetros necesarios
       :param member: objeto de cliente a dar de baja
       :type receiver: dict
       :param reason: motivo de la baja
       :type template: str
       :param unsubscribe_request: es True si el cliente es 'baja' y puede seguir ingresando
       :type unsubscribe_request: bool, optional
       :return: None
       :rtype: None
       """

    status = 'baja' if unsubscribe_request else 'inactivo'

    history_event = create_history_event(member, status, source, reason)

    db.clientes.update_one(
        {"_id": member["_id"]},
        {
            "$push": {
                "history": history_event
            },
            "$set": {
                "next_payment_date": None,
                "status": status
            }
        }
    )

    db.boletas.update_many(
        {
            "member_id": member["_id"],
            "status": {
                "$in": ["error", "rejected", "pending_efectivo", "restored"]
            }
        },
        {
            "$set": {
                "status": status_boleta_inactivado
            }
        }
    )


def create_history_event(member, event_type, source, reason=None):

    if event_type == 'inactivo':
        event_type = 'inactivacion'

    history_event = {
        'event': event_type,
        'date_created': today_argentina(),
        'source': source
    }
    if reason:
        history_event["reason"] = reason

    if event_type in ['alta', 'baja', 'inactivacion', 'revertir_baja']:
        history_event['plan'] = member["active_plan_id"]

        if 'discounts' in member and member["discounts"] and len(member["discounts"]) > 0:
            history_event['discounts'] = member['discounts']

    elif event_type == "cambio_tarjeta":
        history_event["card_id"] = member["active_card"]

    return history_event


def restore_client_from_payment(payment_id: int, sdk: mercadopago.SDK) -> typing.Union[dict, None]:
    """ Método que crea la estructura de un cliente nuevo a partir de un pago de mercadopago.

    :param payment_id: id del pago a analizar
    :type payment_id: int
    :param sdk: sdk de mercadopago para el cual se creo el pago
    :type sdk: mercadopago.SDK
    :return: diccionario de cliente
    :rtype: dict
    """
    payment_response = sdk.payment().get(payment_id)

    if payment_response['status'] >= 400:
        return

    payment = datetime_parser(payment_response['response'])

    try:
        email = payment['additional_info']['items'][0]['description'].split(
            '-')[2].strip().lower()
    except:
        return

    plan = ObjectId(payment['additional_info']['items'][0]['id'])
    nombre = payment['additional_info']['payer']['first_name']
    apellido = payment['additional_info']['payer']['last_name']
    celular = payment['additional_info']['payer']['phone']['number']

    calle = payment['additional_info']['shipments']['receiver_address']['street_name']
    altura = int(payment['additional_info']['shipments']
                 ['receiver_address']['street_number'])
    localidad = payment['additional_info']['shipments']['receiver_address']['city_name']
    provincia = payment['additional_info']['shipments']['receiver_address']['state_name']

    documento = payment['point_of_interaction']['transaction_data']['subscription_id'].split(
        '-')[-1]

    today = today_argentina()
    f_vigencia_apto = today + relativedelta(days=30)

    socio = {
        'nombre': nombre,
        'apellido': apellido,
        'celular': celular,
        'email': email,
        'documento': documento,
        'domicilio': {
            'calle': calle,
            'altura': str(altura),
            'apto_lote': 'n/a',
            'localidad': localidad,
            'provincia': provincia,
            'código postal': '1000'
        },
        'status': 'activo',
        'payment_ids': [payment['id']],
        'last_payment_id': payment['id'],
        'active_plan_id': plan,
        'cobros_recurrentes': 0,
        'nacimiento': '22/02/2022',
        'preferred_payment_method': 'tarjeta',
        'brand_name': 'SportClub',
        'discounts': [],
        'cards': [],
        'apto_medico': {
            'url': '',
            'status': 'pendiente',
            'fecha_vigencia': f_vigencia_apto.replace(day=f_vigencia_apto.day, hour=23, minute=59, second=59)
        },
        'sportaccess_id': f"MUVI-{documento}",
        'poi': {
            'installments': payment['installments'],
            'payment_reference': payment['id']
        }
    }

    # * Dates

    plan = db.planes.find_one({'_id': plan})
    npd = calculate_payment_date(today.day, plan['cobro'], get_periodo(today))
    socio['next_payment_date'] = npd
    socio['fecha_vigencia'] = set_next_vigency(npd)
    socio['last_subscription_date'] = today
    socio['period_init_day'] = today.day

    # * Customer mp

    customer_response = sdk.customer().search({'email': email})['response']
    if customer_response['paging']['total'] == 1:
        customer = customer_response['results'][0]
        customer_id = customer['id']
    else:
        customer_data = {
            "email": email,
            "first_name": nombre,
            "last_name": apellido,
            "phone": {"area_code": None, "number": celular},
            'identification': {'type': 'DNI', 'number': documento},
            'address': {
                'street_name': calle,
                'street_number': altura,
            }
        }
        customer = sdk.customer().create(customer_data)['response']
        if 'email' in customer.keys():
            customer_id = customer['id']
        else:
            customer_id = 'error'

    socio['mercadopago_id'] = customer_id

    # * History

    history_event = create_history_event(
        member=socio, event_type='alta', source='checkout')
    socio['history'] = [history_event]

    # * Plan corporativo

    if plan['price'] == payment['transaction_amount']:
        socio['plan_corporativo'] = None
        plan['corporativo'] = None
    else:
        abandoned = db.abandoned.find_one({'documento': documento})
        try:
            socio['plan_corporativo'] = abandoned['corpo_id']
        except:
            # * No hay forma de recuperar el corporativo que le aplicó un descuento
            return

    return socio


def create_boleta_from_payment(payment_id: int) -> None:
    """ Método que crea una boleta a partir de un payment_id. 
    Para que funcione debe el existir el socio y debe tener el payment_id en su array de payments

    :param payment_id: payment id de mercadopago
    :type payment_id: int
    """

    pipeline = [
        {'$match': {'payment_ids': payment_id}},
        {'$lookup': {
            'from': 'planes',
            'as': 'plan',
            'let': {'active_plan': '$active_plan_id', 'corpo': '$plan_corporativo'},
            'pipeline': [
                {'$project': {
                    'merchant_id': 1,
                    'price': 1
                }},
                {'$match': {
                    '$expr': {
                        '$eq': ['$$active_plan', '$_id']
                    }
                }},
                {'$lookup': {
                    'from': 'corporativo',
                    'as': 'corporativo',
                    'pipeline': [
                        {'$project': {
                            'porcentaje-descuento-empleado': 1,
                            'name': 1
                        }},
                        {'$match': {
                            '$expr': {
                                '$eq': ['$$corpo', '$_id']
                            }
                        }}
                    ]
                }},
                {'$lookup': {
                    'from': 'merchants',
                    'as': 'merchant',
                    'let': {'merchant_id': '$merchant_id'},
                    'pipeline': [
                        {'$project': {
                            'keys.access_token': 1
                        }},
                        {'$match': {
                            '$expr': {
                                '$eq': ['$$merchant_id', '$_id']
                            }
                        }}
                    ]
                }},
                {'$addFields': {
                    'access_token': {
                        '$first': '$merchant.keys.access_token'
                    },
                    'corporativo': {
                        '$first': '$corporativo'
                    }
                }},
                {'$project': {
                    'merchant': 0,
                    'plan_corporativo': 0
                }}
            ]
        }},
        {'$unwind': {'path': '$plan'}},
        {'$project': {
            'documento': 1,
            'cards': 1,
            'discounts': 1,
            'active_plan_id': 1,
            'payment_ids': 1,
            'plan': 1,
            'access_token': '$plan.access_token',
            'corporativo': '$plan.corporativo'
        }},
        {'$project': {
            'plan.access_token': 0,
            'plan.corporativo': 0
        }}
    ]

    client = list(db.clientes.aggregate(pipeline))[0]

    print(f"--- User {client['documento']} ---")
    print('\n')

    sdk = mercadopago.SDK(client['access_token'])

    payment = datetime_parser(sdk.payment().get(payment_id)['response'])

    corpo_discount = 0
    if 'corporativo' in client and client['corporativo']:
        corpo_discount = client['corporativo']['porcentaje-descuento-empleado']

    prices = get_client_price(client=client, corpo_discount=corpo_discount,
                              plan_price=client['plan']['price'], sum_access=False)

    boleta = create_payment_data(_client=client, prices=prices,
                                 merchant_id=client['plan']['merchant_id'], source='checkout3')

    payment_result = {
        'status': payment['status'],
        'status_detail': payment['status_detail'],
        'id': payment['id'],
        'date_created': payment['date_created']
    }

    cards = get_cards(client)
    try:
        card = get_card_data_from_payment(payment)
    except:
        card = cards[0] if cards != [] else get_empty_card()

    update_payment_data(payment_result=payment_result,
                        payment_data=boleta, card_data=card)
    db.boletas.update_one({'_id': boleta['_id']}, {'$set': boleta})
