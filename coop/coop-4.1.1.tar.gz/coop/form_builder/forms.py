from django import forms


class CustomForm(forms.Form):
    def __init__(self, extra_fields, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(extra_fields)
        self.extra_field_names = list(extra_fields.keys())
