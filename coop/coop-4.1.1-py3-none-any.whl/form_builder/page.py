from django.db import models
from wagtail.fields import StreamField

from .blocks import FormStreamBlock
from .views import form_page_view


class ProccessFormMixin(object):
    def get_form_field(self):
        raise NotImplementedError()

    def get_subject(self):
        raise NotImplementedError()

    def get_email_to(self):
        raise NotImplementedError()

    def get_reply_to(self):
        # Usually static not content
        raise NotImplementedError()

    def after_send(self, request, form):
        # Triggered after succesful email
        pass

    def serve(self, request):
        return form_page_view(request, self)


class FormBuilderPageMixin(ProccessFormMixin, models.Model):
    form = StreamField(FormStreamBlock(), use_json_field=True)
    email_subject = models.CharField(max_length=255, help_text='Subject for the automated email')
    email_to = models.EmailField(help_text='Address automated emails are sent to')

    def get_form_field(self):
        return self.form

    def get_subject(self):
        return self.email_subject

    def get_email_to(self):
        return self.email_to

    class Meta:
        abstract = True
