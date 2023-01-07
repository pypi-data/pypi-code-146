from django.http import HttpResponse
from django.utils.translation import gettext as _

from djp_sepa.models import SEPAMandate
from material import Fieldset, Layout, Row
from payments import PaymentStatus

from aleksis.core.forms import ActionForm
from aleksis.core.mixins import ExtensibleForm

from .models.base import Client
from .models.invoice import InvoiceGroup
from .tasks import email_invoice


def send_emails_action(modeladmin, request, queryset):
    """Send e-mails for selected invoices."""
    email_invoice.delay(list(queryset.values_list("token", flat=True)))


send_emails_action.short_description = _("Send e-mails")
send_emails_action.permission = "tezor.send_invoice_email"


def get_sepa_xml(modeladmin, request, queryset):
    """Get a SEPA XML for selected invoices."""
    qs = SEPAMandate.objects.filter(payment__in=queryset, payment__status=PaymentStatus.PREAUTH)
    sepadd = SEPAMandate.as_sepadd(qs=qs)

    return HttpResponse(
        sepadd.export(pretty_print=True).decode(),
        headers={
            "Content-Type": "text/xml",
            "Content-Disposition": 'attachment; filename="sepa_direct_debit.xml"',
        },
    )


get_sepa_xml.short_description = _("Get SEPA XML")
get_sepa_xml.permission = "tezor.get_sepa_xml"


class InvoicesActionForm(ActionForm):
    def get_actions(self):
        return [send_emails_action, get_sepa_xml]


class EditClientForm(ExtensibleForm):
    """Form to create or edit clients."""

    layout = Layout(
        Row("name", "email"),
        Fieldset(
            _("Payment pledge"),
            Row("pledge_enabled"),
        ),
        Fieldset(
            _("Sofort / Klarna"),
            "sofort_enabled",
            Row("sofort_api_id", "sofort_api_key", "sofort_project_id"),
        ),
        Fieldset(
            _("PayPal"),
            "paypal_enabled",
            Row("paypal_client_id", "paypal_secret", "paypal_capture"),
        ),
        Fieldset(
            _("Debit"),
            "sdd_enabled",
            Row("sdd_creditor", "sdd_creditor_identifier"),
            Row("sdd_iban", "sdd_bic"),
        ),
    )

    class Meta:
        model = Client
        exclude = []


class EditInvoiceGroupForm(ExtensibleForm):

    layout = Layout(Row("name", "template_name"))

    class Meta:
        model = InvoiceGroup
        exclude = ["client"]
