"""This file stores some helpful resuable function"""
from .constants import FAC_DEFAULT_CURRENCY 


def format_expiry_date(exp_date, raise_exception=False):
    """
    This function is used to format the expiry date that is sent to the FAC V2 payment gateway
    Parameters:
        exp_date (str): The expire that needs formatting (eg. 09/23)
        raise_exception (bool): Determines if we should raise an exception or return None

    Returns:
        (str): A formatted expiry date
    """
    if exp_date is None or not isinstance(exp_date, str):
        if raise_exception:
            raise ValueError("exp_date is not of type str")
        return None

    exp_date_split = exp_date.split('/')
    
    if len(exp_date_split) != 2:
        raise ValueError("exp_date is in an invalid format")

    # Swap the year and month around
    exp_date = exp_date_split[1] + exp_date_split[0]
    
    return exp_date



"""
Request body generations
"""

def generate_auth_request_body(transaction_detail, card_detail, redirect_url):
    return {
        "TransactionIdentifier": transaction_detail.order_number,
        "TotalAmount": transaction_detail.amount,
        "CurrencyCode": FAC_DEFAULT_CURRENCY,
        "ThreeDSecure": True,
        "Source": {
            "CardPan": card_detail.card_number,
            "CardCvv": card_detail.cvv2,
            "CardExpiration": card_detail.exp_date,
            "CardholderName": card_detail.cardholder_name
        },
        "OrderIdentifier": transaction_detail.order_number,
        "AddressMatch": False,
        "ExtendedData": {
            "ThreeDSecure": {
                "ChallengeWindowSize": 4,
                "ChallengeIndicator": "01"
            },
            "MerchantResponseUrl": redirect_url
        },
        "BrowserInfo": {
            "JavaEnabled": False,
            "JavascriptEnabled": True
        }
    }


def generate_sale_request_body(transaction_detail, card_detail, redirect_url):
    return {
        "TransactionIdentifier": transaction_detail.order_number,
        "TotalAmount": transaction_detail.amount,
        "CurrencyCode": FAC_DEFAULT_CURRENCY,
        "ThreeDSecure": True,
        "Source": {
            "CardPan": card_detail.card_number,
            "CardCvv": card_detail.cvv2,
            "CardExpiration": card_detail.exp_date,
            "CardholderName": card_detail.cardholder_name
        },
        "OrderIdentifier": transaction_detail.order_number,
        "AddressMatch": False,
        "ExtendedData": {
            "ThreeDSecure": {
                "ChallengeWindowSize": 4,
                "ChallengeIndicator": "01"
            },
            "MerchantResponseUrl": redirect_url
        },
        "BrowserInfo": {
            "JavaEnabled": False,
            "JavascriptEnabled": True
        }
    }


def generate_payment_request_body(spiToken):
    return '\"' + spiToken + '\"'


def generate_capture_request_body(transaction_detail):
    return {
        "TotalAmount": transaction_detail.amount,
        "TransactionIdentifier": transaction_detail.order_number
    }


def generate_refund_request_body(transaction_detail):
    return {
        "Refund": True,
        "TransactionIdentifier": transaction_detail.order_number,
        "TotalAmount": transaction_detail.amount,
        "CurrencyCode": FAC_DEFAULT_CURRENCY,
        "Source": {
            "CardPresent": False,
            "CardEmvFallback": False,
            "ManualEntry": False,
            "Debit": False,
            "Contactless": False,
            "CardPan": "",
            "MaskedPan": ""
        },
        "TerminalCode": "",
        "TerminalSerialNumber": "",
        "AddressMatch": False
    }


def generate_void_request_body(order_number):
    return {
        "TransactionIdentifier": order_number,
        "TerminalCode": "",
        "TerminalSerialNumber": "",
        "AutoReversal": False
    }