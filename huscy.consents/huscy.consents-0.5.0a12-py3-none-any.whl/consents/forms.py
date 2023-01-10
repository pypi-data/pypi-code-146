from django import forms
from django.utils import timezone
from jsignature.forms import JSignatureField

from huscy.consents.models import Consent


class CreateConsentForm(forms.ModelForm):
    class Meta:
        model = Consent
        fields = 'name', 'text_fragments'


class SelectDateWidget(forms.SelectDateWidget):
    template_name = 'consents/widgets/select_date.html'


class DateOfBirthField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs['initial'] = timezone.now().date() + timezone.timedelta(days=1)
        kwargs['widget'] = SelectDateWidget(
            years=range(timezone.now().year, timezone.now().year - 120, -1),
        )
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if value > timezone.datetime.today().date():
            raise forms.ValidationError('The date of birth mustn\'t be in the future!')


class ContactDataForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    postal_code = forms.CharField()
    phone_number = forms.CharField()
    email = forms.EmailField()
    date_of_birth = DateOfBirthField()


class SignatureForm(forms.Form):
    signature = JSignatureField()


class ConsentForm(ContactDataForm, SignatureForm):
    pass
