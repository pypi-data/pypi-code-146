
from django import forms
from django.utils.translation import gettext_lazy as _

from orders.models import Order

from delivery.fields import DeliveryFormField


class CheckoutForm(forms.ModelForm):

    delivery = DeliveryFormField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['delivery'].init_form(*args, **kwargs)

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if mobile.startswith('+3800'):
            raise forms.ValidationError(
                _('Phone number could not start with `+3800`'))
        return mobile

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'middle_name', 'payment_method',
            'mobile', 'comment'
        ]
