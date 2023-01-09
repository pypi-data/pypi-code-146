from django.core.mail import EmailMessage
from django.forms.fields import FileField
from django.template.response import TemplateResponse
from honeypot.decorators import check_honeypot

from coop.utils.forms import form_data_to_text


@check_honeypot
def form_page_view(request, form_page, *args, **kwargs):
    form_block = None
    field_blocks = []
    if hasattr(form_page.get_form_field().stream_block, 'get_form'):
        # Form only streamfield
        form_block = form_page.get_form_field().stream_block
        field_blocks = form_page.get_form_field()
    else:
        # It's in a child block, let's go searching
        for child in form_page.get_form_field():
            if hasattr(child.block, 'get_form'):
                form_block = child.block
                field_blocks = [b for b in child.value]
                break

    context = form_page.get_context(request, *args, **kwargs)

    if request.method == 'POST' and form_block and field_blocks:
        form = form_block.get_form(field_blocks, data=request.POST, files=request.FILES)

        if form.is_valid():
            msg_content = '\nForm page title:\n{0}'.format(form_page.title)
            msg_content += '\n\nForm page URL:\n{0}'.format(form_page.full_url)
            msg_content += '\n\nSee form submission data below'
            msg_content += '\n------------------------------'
            msg_content += form_data_to_text(form)
            msg_content += '\n\n------------------------------'
            msg_content += '\nThis is an automated message, please do not reply.'

            msg = EmailMessage(
                form_page.get_subject(), msg_content,
                to=[form_page.get_email_to()],
                reply_to=[form_page.get_reply_to()]
            )

            for bound_field in form:
                name = bound_field.name
                if isinstance(bound_field.field, FileField) and name in request.FILES:
                    file = request.FILES[name]
                    msg.attach(file.name, file.read(), file.content_type)
            msg.send()

            form_page.after_send(request, form)
            context.update({
                'completed': True
            })
    elif form_block and field_blocks:
        form = form_block.get_form(field_blocks)
    else:
        form = None

    context.update({
        'form': form
    })
    return TemplateResponse(request, form_page.get_template(request, *args, **kwargs), context)
