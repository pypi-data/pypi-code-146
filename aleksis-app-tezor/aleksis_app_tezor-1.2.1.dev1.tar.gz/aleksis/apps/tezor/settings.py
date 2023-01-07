INSTALLED_APPS = ["payments", "djp_sepa"]

PAYMENT_MODEL = "tezor.Invoice"
PAYMENT_VARIANT_FACTORY = "aleksis.apps.tezor.util.invoice.provider_factory"

overrides = ["PAYMENT_MODEL", "PAYMENT_VARIANT_FACTORY"]
