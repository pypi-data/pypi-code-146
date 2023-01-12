import requests
from entities import TransactionDetail
from .constants import (
    FAC_V2_BASE_URL,
    FAC_V2_HEADERS_JSON,
    FAC_V2_HEADERS_PLAIN_TEXT,
    TransactionType,
)
from .utils import (
    generate_auth_request_body,
    generate_capture_request_body,
    generate_payment_request_body,
    generate_sale_request_body,
    generate_void_request_body,
    generate_refund_request_body
)


def authorize(transaction_detail, card_detail, redirect_url):
    endpoint = "spi/Auth"
    url = FAC_V2_BASE_URL + endpoint
    request_body = generate_auth_request_body(transaction_detail, card_detail, redirect_url)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=request_body)

    return response

def sale(transaction_detail, card_detail, redirect_url):
    endpoint = "spi/Sale"
    url = FAC_V2_BASE_URL + endpoint
    request_body = generate_sale_request_body(transaction_detail, card_detail, redirect_url)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=request_body)

    return response

def payment(spi_token: str):
    endpoint = "spi/Payment"
    url = FAC_V2_BASE_URL + endpoint
    request_body = generate_payment_request_body(spi_token)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_PLAIN_TEXT, data=request_body)

    return response

def capture(transaction_detail: TransactionDetail):
    endpoint = "Capture"
    url = FAC_V2_BASE_URL + endpoint
    request_body = generate_capture_request_body(transaction_detail)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=request_body)

    return response

def refund(transaction_detail: TransactionDetail):
    endpoint = "Refund"
    url = FAC_V2_BASE_URL + endpoint
    request_body = generate_refund_request_body(transaction_detail)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=request_body)

    return response

def void(order_number: str):
    endpoint = "Void"
    url = FAC_V2_BASE_URL + endpoint
    void_request_body = generate_void_request_body(order_number)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=void_request_body)

    return response


def reverse(transaction):
    response = None

    if transaction.transaction_type == TransactionType.AUTH.value:
        response = void(order_number=transaction.order_id)
    elif transaction.transaction_type == TransactionType.SALE.value:
        transaction_detail = TransactionDetail(order_number=transaction.order_id, amount=transaction.total_payment)
        response = refund(transaction_detail=transaction_detail)
    
    return response
