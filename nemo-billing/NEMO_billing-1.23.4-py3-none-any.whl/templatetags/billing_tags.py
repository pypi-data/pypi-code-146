from typing import Iterable

from django import template

from NEMO_billing.invoices.utilities import display_amount as amount

register = template.Library()


@register.filter
def display_amount(value, configuration=None):
    if value is not None and configuration:
        return amount(value, configuration)


@register.filter
def to_dict(value: Iterable, attribute=None):
    return {getattr(item, attribute, None): item for item in value}
