# Expected Payment's direction
class DirectionTypes:
    CREDIT = 'credit'
    DEBIT = 'debit'

# PaymentOrders
class PaymentOrderTypes:
    ACH = 'ach'
    WIRE = 'wire'
    CHECk = 'check'
    BOOK = 'book'
    rtp = 'rtp'

# account types
class AccountTypes:
    CHECKING = 'checking'
    SAVINGS = 'savings'
    OTHER = 'other'


class AccountNumberType:
    IBAN = 'iban'
    CLABE = 'clabe'
    OTHER = 'other'


class RoutingNumberTypes:
    # routing number types
    ABA = 'aba'
    SWIFT = 'swift'
    CPA = 'ca_cpa'
    BSB = 'au_bsb'
    GB = 'gb_sort_code'
    IFSC = 'in_ifsc'


def mask_number(s):
    return s[-4:].rjust(len(s), "*")
