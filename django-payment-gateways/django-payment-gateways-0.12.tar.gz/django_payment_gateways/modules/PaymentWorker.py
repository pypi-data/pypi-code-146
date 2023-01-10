from importlib import import_module

from django.conf import settings

from django_payment_gateways.exceptions import DriverNotFoundException, InvoiceNotFoundException
from django_payment_gateways.modules.abstracts import Driver
from django_payment_gateways.modules.invoice import Invoice

gateway_cache = {}


class PaymentWorker:
    _driver_instance: Driver = None
    _invoice: Invoice = None

    def __init__(self):
        self.config = self._get_default_config()
        self._invoice = Invoice()
        self.via(self.get_default_driver())

    def _get_default_config(self) -> dict:
        return getattr(settings, 'PAYMENT_SETTINGS', {})

    def get_default_driver(self) -> str:
        return self.config['drivers']['default']

    def get_driver_config(self, driver) -> dict:
        return self.config['drivers'][driver]

    def via(self, driver):
        self.driver = driver
        self.validate_driver()
        self._invoice.via(driver)
        self.settings = self.get_driver_config(driver)

    def validate_driver(self):
        if not self.driver:
            raise DriverNotFoundException('Driver not selected or default driver does not exist.')

        if not self.config['drivers'][self.driver] or not self.config['map'][self.driver]:
            raise DriverNotFoundException('Driver not found in config file. Try updating the package.');

    def validate_invoice(self):
        if not self._invoice:
            raise InvoiceNotFoundException('Invoice not selected or does not exist.')

    def set_amount(self, amount):
        self._invoice.set_amount(amount)

    def set_invoice(self, invoice):
        self._invoice = invoice

    def set_callback(self, callback_url):
        self.settings['callbackUrl'] = callback_url

    def purchase(self, invoice: Invoice = None):
        if invoice:
            self._invoice = invoice

        self._driver_instance = self.get_fresh_driver_instance()

        transaction_id = self._driver_instance.purchase()
        return self._driver_instance, transaction_id

    def pay(self):
        self._driver_instance = self.get_driver_instance()
        self.validate_invoice()
        return self._driver_instance.pay()

    def verify(self, request):
        self._driver_instance = self.get_driver_instance()
        self.validate_invoice()
        receipt = self._driver_instance.verify(request)
        return receipt, self._driver_instance

    def get_driver_instance(self):
        if self._driver_instance:
            return self._driver_instance

        return self.get_fresh_driver_instance()

    def get_fresh_driver_instance(self):
        self.validate_driver()
        klass = self.import_driver()
        return klass(self._invoice, self.settings)

    def import_driver(self):
        """
        Return a gateway instance specified by `gateway` name.
        This caches gateway classes in a module-level dictionnary to avoid hitting
        the filesystem every time we require a gateway.
        Should the list of available gateways change at runtime, one should then
        invalidate the cache, the simplest of ways would be to:
        >>> gateway_cache = {}
        """
        # Is the class in the cache?
        clazz = gateway_cache.get(self.driver, None)
        if not clazz:
            # Let's actually load it (it's not in the cache)
            str_mod: str = self.config['map'][self.driver]
            module_name, class_name = str_mod.split(':')
            clazz = getattr(import_module(module_name), class_name)
            gateway_cache[self.driver] = clazz
        return clazz
