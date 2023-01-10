from abc import ABC, abstractmethod

from django_payment_gateways.modules.invoice import Invoice


class Driver(ABC):

    @abstractmethod
    def __init__(self, invoice: Invoice, settings: dict):
        pass

    def set_amount(self, amount):
        self.amount = amount

    def set_invoice(self, invoice: Invoice):
        self.invoice = invoice

    @abstractmethod
    def purchase(self):
        pass

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def verify(self, request):
        pass
