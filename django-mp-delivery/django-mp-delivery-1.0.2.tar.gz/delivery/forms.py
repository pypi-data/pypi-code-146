
from django import forms
from django.utils.translation import gettext_lazy as _

from delivery.models import DeliveryMethod


class DeliveryForm(forms.Form):

    delivery_method = forms.ModelChoiceField(
        label=_('Delivery method'),
        queryset=DeliveryMethod.objects.filter(
            # Hotfix to leave only two methods
            code__in=['self_delivery', 'novaposhta']
        ))

    city = forms.CharField(
        label=_('City'),
        required=False
    )

    warehouse = forms.CharField(
        label=_('Warehouse'),
        required=False
    )

    @property
    def delivery_methods(self):
        return {m.code: m.id for m in DeliveryMethod.objects.all()}
