# django
from django.utils.translation import ugettext_lazy as _


class CurrencyAcronyms:
    CLF = "CLF"
    USD = "USD"
    EUR = "EUR"
    CLP = "CLP"

    django_model_choices = (
        (CLP, _("CLP")),
        (CLF, _("CLF")),
        (USD, _("USD")),
        (EUR, _("EUR")),
    )
