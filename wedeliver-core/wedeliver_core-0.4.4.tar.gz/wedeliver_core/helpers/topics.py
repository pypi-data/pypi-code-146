from enum import Enum


class Topics(Enum):
    SEND_MAIL = 'send_mail'
    SEND_SMS = 'send_sms'
    SEND_PUSH_NOTIFICATION = 'send_push'
    INTERNAL_NOTIFICATION_MESSAGE = 'internal_notification_message'
    CREATE_STC_SUPPLIER_PAYMENT_TRANSACTION = 'create_stc_supplier_payment_transaction'
    CREATE_ANB_PAYMENT_TRANSACTION = 'create_anb_payment_transaction'
    CREATE_INSTALLMENTS = 'create_installments'
