from django.forms.fields import BooleanField, MultipleChoiceField


def form_data_to_text(form, html=False):
    """ Helper method to turn a form response to a text (usually for email) """
    data_string = ""

    for bound_field in form:
        if isinstance(bound_field.field, BooleanField):
            value = form.cleaned_data[bound_field.name]
            value_display = 'Yes' if value else 'No'
            if html:
                data_string += f'<p>{bound_field.label}: {value_display}</p>'
            else:
                data_string += f'\n\n{bound_field.label}: {value_display}'
        elif isinstance(bound_field.field, MultipleChoiceField):
            values = form.cleaned_data[bound_field.name]
            if html:
                data_string += f'<p>{bound_field.label}:'
            else:
                data_string += f'\n\n{bound_field.label}:'
            for choice in bound_field.field.choices:
                value_display = 'Yes' if choice[0] in values else 'No'
                if html:
                    data_string += f'<br/>{choice[0]} - {value_display}'
                else:
                    data_string += f'\n{choice[0]} - {value_display}'
            if html:
                data_string += '</p>'
        else:
            value = form.cleaned_data[bound_field.name]
            if not value:
                value = 'Not filled out.'
            if html:
                data_string += f'<p>{bound_field.label}:<br/>{value}</p>'
            else:
                data_string += f'\n\n{bound_field.label}:\n{value}'

    return data_string
