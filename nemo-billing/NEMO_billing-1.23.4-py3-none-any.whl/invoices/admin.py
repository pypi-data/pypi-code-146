from NEMO.admin import ProjectAdmin
from NEMO.models import Project
from django.apps import apps
from django.contrib import admin
from django.contrib.admin import SimpleListFilter, register
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Length
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html

from NEMO_billing.invoices.models import (
    Invoice,
    InvoiceConfiguration,
    InvoiceDetailItem,
    InvoicePayment,
    InvoiceSummaryItem,
    ProjectBillingDetails,
)
from NEMO_billing.invoices.views.invoices import review_invoice, send_invoice, void_invoice, zip_response


def clone_configuration(configuration: InvoiceConfiguration):
    """
    Create a clone of selected configurations and save them.

    :param configuration:
    :return: Newly cloned configuration
    """
    configuration.pk = None
    configuration.name = f"Copy of {configuration.name}"
    configuration.save()

    return configuration


def clone_configurations(modeladmin, request, queryset):
    for configuration in queryset.all():
        clone_configuration(configuration)


clone_configurations.short_description = "Clone selected Configurations"


def email_invoices(modeladmin, request, queryset):
    for invoice in queryset.all():
        send_invoice(request, invoice.id)


email_invoices.short_description = "Email selected invoices to customers"


def review_invoices(modeladmin, request, queryset):
    for invoice in queryset.all():
        review_invoice(request, invoice.id)


review_invoices.short_description = "Mark selected invoices as reviewed"


def void_invoices(modeladmin, request, queryset):
    for invoice in queryset.all():
        void_invoice(request, invoice.id)


void_invoices.short_description = "Mark selected invoices as void"


def zip_invoices(modeladmin, request, queryset):
    return zip_response(request, queryset.all())


zip_invoices.short_description = "Download selected invoices"


class InvoiceSummaryItemInline(admin.TabularInline):
    model = InvoiceSummaryItem
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class InvoiceDetailItemInline(admin.TabularInline):
    model = InvoiceDetailItem
    can_delete = False
    exclude = ("content_type", "object_id")
    readonly_fields = ("get_item",)
    fields = ("get_item", "core_facility", "item_type", "name", "quantity", "start", "end", "user", "rate", "amount")

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description="Item")
    def get_item(self, obj: InvoiceDetailItem):
        if not obj.content_type or not obj.object_id:
            return "-"
        app_label, model = obj.content_type.app_label, obj.content_type.model
        viewname = f"admin:{app_label}_{model}_change"
        try:
            args = [obj.object_id]
            link = reverse(viewname, args=args)
        except NoReverseMatch:
            return "-"
        else:
            return format_html(
                '<a href="{}">{} - #{}</a>', link, self.get_model_name(obj.content_type), obj.object_id
            )

    def get_model_name(self, content_type: ContentType):
        try:
            model = apps.get_model(content_type.app_label, content_type.model)
            return model._meta.verbose_name.capitalize()
        except (LookupError, AttributeError):
            return ""


class InvoiceStatusFilter(SimpleListFilter):
    title = "status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("unsent-reviewed", "Reviewed, not sent"),
            ("sent", "Sent"),
            ("unsent", "Not sent"),
            ("reviewed", "Reviewed"),
            ("unreviewed", "Not reviewed"),
            ("voided", "Voided"),
        ]

    def queryset(self, request, queryset):
        new_queryset = Invoice.objects.filter(voided_date=None)
        if self.value() in ["unsent-reviewed", "unsent"]:
            new_queryset = new_queryset.filter(sent_date=None)
        if self.value() in ["reviewed", "unsent-reviewed"]:
            new_queryset = new_queryset.filter(reviewed_date__isnull=False)
        if self.value() == "sent":
            new_queryset = new_queryset.filter(sent_date__isnull=False)
        if self.value() == "unreviewed":
            new_queryset = new_queryset.filter(reviewed_date=None)
        if self.value() == "voided":
            new_queryset = Invoice.objects.filter(voided_date__isnull=False)
        return new_queryset


@register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceSummaryItemInline, InvoiceDetailItemInline)
    list_display = (
        "invoice_number",
        "get_total_amount_currency",
        "get_tax_display",
        "project_details",
        "configuration",
        "created_date",
        "due_date",
        "last_sent_date",
        "reviewed_date",
        "voided_date",
        "file",
    )
    list_filter = (InvoiceStatusFilter, "start", "due_date", "configuration__currency", "project_details__project__name")
    ordering = (Length("invoice_number").desc(), "-invoice_number")
    readonly_fields = ("created_by", "created_date")
    date_hierarchy = "start"
    search_fields = ["invoice_number", "project_details__project__name"]
    actions = (email_invoices, review_invoices, void_invoices, zip_invoices)

    @admin.display(description="Amount", ordering="total_amount")
    def get_total_amount_currency(self, obj: Invoice):
        return obj.total_amount_display()

    @admin.display(description="Tax")
    def get_tax_display(self, obj: Invoice):
        return obj.tax_display()


@register(InvoiceConfiguration)
class InvoiceConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "merchant_name", "currency")
    ordering = ("name",)
    actions = (clone_configurations,)
    fieldsets = (
        (None, {"fields": ("name", "invoice_due_in", "detailed_invoice")}),
        ("Communication", {"fields": ("email_from", "email_cc", "reminder_frequency")}),
        ("Merchant info", {"fields": ("merchant_name", "merchant_details", "merchant_logo", "terms")}),
        ("Currency", {"fields": ("currency", "currency_symbol")}),
        ("Tax", {"fields": ("tax_name", "tax")}),
        (
            "Display charges",
            {
                "fields": (
                    "separate_tool_usage_charges",
                    "separate_area_access_charges",
                    "separate_staff_charges",
                    "separate_consumable_charges",
                    "separate_missed_reservation_charges",
                    "separate_training_charges",
                    "separate_custom_charges",
                )
            },
        ),
    )


@register(InvoicePayment)
class InvoicePaymentAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by", "created_date", "updated_by", "updated_date")
    list_display = ("invoice", "payment_received", "payment_processed", "get_amount_display", "updated_by", "updated_date")
    list_filter = ("payment_received", "payment_processed", "invoice__project_details__project__name", "invoice")
    date_hierarchy = "payment_received"

    @admin.display(description="Amount", ordering="amount")
    def get_amount_display(self, obj: InvoicePayment):
        return obj.amount_display()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class ProjectBillingDetailsInline(admin.StackedInline):
    model = ProjectBillingDetails
    can_delete = False
    verbose_name_plural = "details"


class NewProjectAdmin(ProjectAdmin):
    inlines = ProjectAdmin.inlines + (ProjectBillingDetailsInline,)


# Re-register ProjectAdmin
admin.site.unregister(Project)
admin.site.register(Project, NewProjectAdmin)
