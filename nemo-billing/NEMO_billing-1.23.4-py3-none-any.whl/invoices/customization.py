from datetime import datetime
from typing import Dict

from NEMO.decorators import customization
from NEMO.utilities import get_month_timeframe
from NEMO.views.customization import CustomizationBase
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template import Context, Template


@customization(key="invoices", title="Invoices")
class InvoiceCustomization(CustomizationBase):
    variables = {
        "invoice_number_format": "{:04d}",
        "invoice_number_current": "0",
        "invoice_zip_export_template": "{{ account_name }}/{{ project_name }}-{{ invoice.start|date:'Y' }}-{{ invoice.start|date:'F' }}-{{ invoice.invoice_number|slugify }}",
        "invoice_month_list_since": "",
        "invoice_list_hide_created_date": "",
        "invoice_list_hide_month": "",
        "invoice_list_hide_sent_date": "",
        "invoice_list_hide_due_date": "",
        "invoice_list_hide_review_date": "",
        "invoice_list_hide_tax": "",
        "invoice_list_hide_outstanding": "",
        "invoice_list_hide_actions": "",
    }
    files = [
        ("email_send_invoice_subject", ".txt"),
        ("email_send_invoice_message", ".html"),
        ("email_send_invoice_reminder_subject", ".txt"),
        ("email_send_invoice_reminder_message", ".html"),
    ]

    @classmethod
    def hide_column_names(cls):
        return [var.replace("invoice_list_hide_", "") for var in cls.variables if var.startswith("invoice_list_hide") and cls.get_bool(var)]

    def context(self) -> Dict:
        # Adding invoice number formatted to the template
        customization_context = super().context()
        try:
            customization_context["invoice_number_formatted"] = self.get("invoice_number_format").format(
                int(self.get("invoice_number_current"))
            )
        except:
            pass
        try:
            customization_context["invoice_zip_template_formatted"] = self.invoice_template_validation_context(self.get("invoice_zip_export_template")) + ".pdf"
        except:
            pass
        return customization_context

    def validate(self, name, value):
        if name == "invoice_number_format":
            try:
                value.format(123)
            except Exception as e:
                raise ValidationError(str(e))
        elif name == "invoice_zip_export_template":
            try:
                self.invoice_template_validation_context(value)
            except Exception as e:
                raise ValidationError(str(e))
        elif name == "invoice_month_list_since" and value:
            self.validate_date(value)

    def invoice_template_validation_context(self, value):
        from NEMO_billing.invoices.models import Invoice
        invoice = Invoice()
        invoice.invoice_number = invoice.generate_invoice_number()
        invoice_date = datetime.now().replace(month=datetime.now().month-1)
        invoice.start, invoice.end = get_month_timeframe(invoice_date.isoformat())
        invoice.created_date = datetime.now()
        return Template(value).render(Context({"invoice": invoice, "project_name": "test-project", "account_name": "test-account"}))


@customization(key="billing", title="Billing")
class BillingCustomization(CustomizationBase):
    variables = {
        "billing_accounting_email_address": "",
        "billing_project_expiration_reminder_days": "",
        "billing_project_expiration_reminder_cc": "",
    }
    files = [
        ("billing_project_expiration_reminder_email_subject", ".txt"),
        ("billing_project_expiration_reminder_email_message", ".html"),
    ]

    def validate(self, name, value):
        if name == "billing_project_expiration_reminder_days" and value:
            # Check that we have an integer or a list of integers
            try:
                for reminder_days in value.split(","):
                    try:
                        int(reminder_days)
                    except ValueError:
                        raise ValidationError(f"{reminder_days} is not a valid integer")
            except ValidationError:
                raise
            except Exception as e:
                raise ValidationError(str(e))
        elif name == "billing_accounting_email_address" and value:
            validate_email(value)
        elif name == "billing_project_expiration_reminder_cc":
            recipients = tuple([e for e in value.split(",") if e])
            for email in recipients:
                validate_email(email)
