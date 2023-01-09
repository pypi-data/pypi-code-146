from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea())
