from .utils import format_expiry_date

class CardDetail:
    def __init__(self, card_number, cvv2, exp_date, cardholder_name):
        self.card_number = card_number
        self.cvv2 = cvv2
        self.exp_date = exp_date
        self.cardholder_name = cardholder_name

    @property
    def formatted_exp_date(self):
        return format_expiry_date(self.exp_date)

class TransactionDetail:
    def __init__(self, order_number, amount):
        self.order_number = order_number
        self.amount = amount
