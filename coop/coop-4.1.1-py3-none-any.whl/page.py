import re

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template.response import TemplateResponse
from wagtail import models as wagtailmodels
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtailmetadata.models import MetadataPageMixin

from .forms import ContactForm


class Page(MetadataPageMixin, wagtailmodels.Page):
    """
    A base page with social metadata and a more sensible default template.
    """

    # Disable the creation of the related field accessor on Page
    # This prevents conflicts with model names and field names
    page_ptr = models.OneToOneField(wagtailmodels.Page, parent_link=True,
                                    related_name='+', on_delete=models.CASCADE)

    # We override promote panels to remove show_in_menus
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('search_image'),  # From MetadataPageMixin
        ], 'Common page configuration'),
    ]

    def get_template(self, request, *args, **kwargs):
        """
        Templates are named like ``layouts/app/model.html``.
        """
        label = self._meta.label.split('.')
        app = label[0]
        model_name = '_'.join(re.findall('^[a-z]+|[A-Z][^A-Z]*', label[1])).lower()
        return "layouts/{}/{}.html".format(app, model_name)

    def get_object_title(self):
        site = self.get_site()
        return f'{self.get_meta_title()} | {site.site_name}'

    class Meta:
        abstract = True


class ContactPageMixin(models.Model):
    contact_form_class = ContactForm

    email_to = models.EmailField(help_text='The email address enquiries should be sent to')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({
            'gmaps_key': getattr(settings, 'GMAPS_KEY', ''),
        })
        return context

    def send_email(self, form):
        data = form.cleaned_data
        msg_content = '\n'.join([
            '{0}: {1}'.format(field.label, data[field.name])
            for field in form])
        msg = EmailMessage(
            'Website enquiry from %s' % data['name'], msg_content,
            to=[self.email_to],
            reply_to=[data['email']])
        msg.send()

    def serve(self, request):
        request.is_preview = getattr(request, 'is_preview', False)
        context = self.get_context(request)
        ContactFormClass = self.contact_form_class

        if request.method == 'POST':
            form = ContactFormClass(request.POST)
            if form.is_valid():
                self.send_email(form)
            context.update({
                'success': form.is_valid(),
            })
        else:
            form = ContactFormClass()

        context.update({
            'contact_form': form
        })
        return TemplateResponse(request, self.get_template(request), context)

    class Meta:
        abstract = True
