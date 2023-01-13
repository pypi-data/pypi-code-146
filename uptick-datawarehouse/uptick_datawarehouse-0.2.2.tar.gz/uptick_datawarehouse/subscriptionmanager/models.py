# Create your models here.
import decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .. import model_settings


class PaymentMethodSummary(models.Model):
    """Dump payment methods to the data warehouse."""

    last_synced = models.DateTimeField()
    customer_account_number = models.CharField(max_length=50)
    gocardless_id = models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_paymentmethod_summary'



class RevenueForecastSummary(models.Model):
    """Dump payment methods to the data warehouse."""

    last_synced = models.DateTimeField()
    month = models.DateField()
    total_contract_value = models.DecimalField(max_digits=10, decimal_places=2)
    total_credit_value = models.DecimalField(max_digits=10, decimal_places=2)
    signed_value = models.DecimalField(max_digits=10, decimal_places=2)
    starting_value = models.DecimalField(max_digits=10, decimal_places=2)
    subs_total = models.IntegerField()
    subs_total_paying = models.IntegerField()
    subs_starting = models.IntegerField()
    subs_won = models.IntegerField()
    subs_lost = models.IntegerField()

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_revenueforecast_summary'



class SubscriptionSummary(models.Model):
    """Dump data to the data warehouse so that it can be used by other reporting or internal tools like Vitally."""

    last_synced = models.DateTimeField()

    created = models.DateTimeField()
    updated = models.DateTimeField()
    salesperson = models.CharField(max_length=200)
    product = models.CharField(max_length=200)

    # customer details
    customer_name = models.CharField(max_length=200)
    customer_account_number = models.CharField(max_length=50, unique=True)
    customer_xero_guid = models.UUIDField(blank=True)
    customer_primary_contact_name = models.CharField(max_length=200)
    customer_primary_contact_email = models.CharField(max_length=200)
    customer_accounts_contact_name = models.CharField(max_length=200)
    customer_accounts_contact_email = models.CharField(max_length=200)
    customer_company_tax_number = models.CharField(max_length=50, help_text="ABN, NZBN or VAT number.")

    # subscriptions
    subscription_guid = models.UUIDField()
    currency = models.CharField(max_length=3)
    signing_date = models.DateField()
    billing_date = models.DateField()

    plan = models.CharField(max_length=100)
    staff_addon_name = models.CharField(max_length=100)

    plan_included_licenses = models.IntegerField(blank=True, null=True)
    additional_committed_staff = models.IntegerField(blank=True, null=True)
    total_contracted_staff_licenses = models.IntegerField(blank=True, null=True)

    override_plan_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    override_staff_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    effective_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_contract_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # addons
    hosting_addon_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bi_addon_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sla_addon_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # workspaces
    workspaces = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    # termination
    termination_date = models.DateField(blank=True, null=True)
    termination_code = models.TextField(blank=True)
    termination_reason = models.TextField(blank=True)

    # current usage data
    current_expansion_chargeable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_total_mrr_chargeable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_total_used_staff_licenses = models.IntegerField(blank=True, null=True)
    current_total_additional_chargable_licenses = models.IntegerField(blank=True, null=True)
    current_monthly_recurring_credit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # last month usage data
    lastmonth_expansion_charged = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lastmonth_total_mrr_charged = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lastmonth_total_used_staff_licenses = models.IntegerField(blank=True, null=True)
    lastmonth_total_used_desk_licenses = models.IntegerField(blank=True, null=True)
    lastmonth_total_used_field_licenses = models.IntegerField(blank=True, null=True)
    lastmonth_total_additional_chargable_licenses = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_subscription_summary'


class RecurringCreditSummary(models.Model):
    """Dump data to the data warehouse so that it can be used by other reporting or internal tools like Vitally."""

    last_synced = models.DateTimeField()

    subscription_guid = models.UUIDField()
    customer_name = models.CharField(max_length=200)
    customer_account_number = models.CharField(max_length=50, unique=True)
    currency = models.CharField(max_length=3)

    start_date = models.DateField()
    review_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_text = models.CharField(max_length=200)
    internal_note = models.CharField(max_length=500, blank=True)
    credit_classification = models.TextField()

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_recurring_credit_summary'


class ChangeSummary(models.Model):
    """Dump data to the data warehouse so that it can be used by other reporting or internal tools like Vitally."""

    last_synced = models.DateTimeField()

    subscription_guid = models.UUIDField()
    customer_name = models.CharField(max_length=200)
    customer_account_number = models.CharField(max_length=50, unique=True)
    currency = models.CharField(max_length=3)

    change_type = models.TextField()
    date = models.DateField()
    note = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    salesperson = models.CharField(max_length=200)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_change_summary'


class ChargeSummary(models.Model):
    """Dump data to the data warehouse so that it can be used by other reporting or internal tools like Vitally."""

    last_synced = models.DateTimeField()

    created = models.DateTimeField()
    updated = models.DateTimeField()
    requestor = models.CharField(max_length=200)

    subscription_guid = models.UUIDField()
    customer_name = models.CharField(max_length=200)
    customer_account_number = models.CharField(max_length=50, unique=True)
    currency = models.CharField(max_length=3)

    itemcode = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    account_code = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tracking_category_1 = models.CharField(max_length=50)
    tracking_category_2 = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    invoice_date = models.DateField(null=True)
    invoice_reference = models.CharField(null=True, max_length=20)
    invoice_number = models.CharField(null=True, max_length=20)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_charge_summary'


class WorkspaceSummary(models.Model):
    """Dump data to the data warehouse so that any other tools can map workspaces back to customers and subscriptions.
    """

    last_synced = models.DateTimeField()

    guid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    customer_account_number = models.CharField(max_length=50, unique=True)
    subscription_guid = models.UUIDField()

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_workspace_summary'


class XeroContactSummary(models.Model):
    """Dump data to the data warehouse so that it can be used by other reporting or internal tools like Vitaly."""

    last_synced = models.DateTimeField()

    customer_name = models.CharField(max_length=200)
    customer_account_number = models.CharField(max_length=50)
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_xero_customer_summary'


class XeroInvoiceSummary(models.Model):
    """Dump data to the data warehouse so that it can be used by other reporting or internal tools like Vitaly."""

    last_synced = models.DateTimeField()

    invoice_guid = models.UUIDField()
    contact_guid = models.UUIDField()
    contact_name = models.CharField(max_length=200)
    contact_account_number = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal("0.00"))
    status = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal("0.00"))
    is_sent = models.BooleanField()
    repeating_invoice_guid = models.UUIDField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal("0.00"))
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal("0.00"))
    fully_paid_on_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'subscriptionmanager'

        default_permissions = ()
        db_table = 'subscriptionmanager"."billing_xero_invoice_summary'

