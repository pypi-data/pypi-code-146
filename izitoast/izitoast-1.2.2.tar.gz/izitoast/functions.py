from django.template.loader import render_to_string
from django.contrib import messages


def izitoast(request, model, message, diversify=None):
    if type(message) == str:
        message = str_to_dict(model=model, message=message)

    template = None
    create_content = None
    if model == "success":
        template = 'custom_response/mul-success-response.txt'
    elif model == "info":
        template = 'custom_response/mul-info-response.txt'
    elif model == "warning":
        template = 'custom_response/mul-warning-response.txt'
    elif model == "danger":
        template = 'custom_response/mul-error-response.txt'
    elif model == "form-error":
        create_content = message
        str_diversify = render_to_string(template_name='custom_response/diversify.txt',
                                         context=diversify)
        str_diversify = str(str_diversify)
        create_content = str(create_content)
        create_content += str_diversify
    if model != "form-error":
        create_content = render_to_string(template_name=template, context=message)
        create_content += render_to_string(template_name='custom_response/diversify.txt',
                                           context=diversify)

    if model == "success":
        return messages.success(request=request, message=create_content)
    elif model == "info":
        return messages.info(request=request, message=create_content)
    elif model == "warning":
        return messages.warning(request=request, message=create_content)
    elif model == "danger":
        return messages.error(request=request, message=create_content)
    elif model == "form-error":
        return messages.error(request=request, message=create_content)


def str_to_dict(model, message):
    message_dict = {
        'raw': [
            {
                'tag': model,
                'item': message
            }
        ]
    }
    return message_dict
