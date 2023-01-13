from django.contrib.postgres.fields import ArrayField
from django.db import models

from .. import model_settings


class WorkforceAddressSummary(models.Model):
    class Countries(models.TextChoices):
        AU = "AU", "Australia"
        NZ = "NZ", "New Zealand"

    tenant = models.CharField(db_index=True, max_length=200)
    last_synced = models.DateTimeField()
    prop_status = models.CharField(max_length=30, blank=True)
    prop_id = models.IntegerField()
    prop_created = models.DateTimeField()
    address = models.CharField(max_length=1000, blank=True, help_text="Exact and validated registered postal address.")
    display = models.TextField(max_length=1000, blank=False, help_text="Address that will be used for display purposes.")
    country = models.CharField(max_length=2, blank=True, default="AU", choices=Countries.choices)
    gnaf_id = models.CharField(max_length=30, default="", blank=True)
    state = models.CharField(max_length=50, blank=True, default="", verbose_name="State or Region")
    postal_code = models.CharField(max_length=15, blank=True, default="", verbose_name="Postal or Zip code")
    coords = models.CharField(max_length=40, blank=True)
    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        default_permissions = ()
        db_table = 'workforce"."address_summary'


# Constance settings
class ConstanceSetting(models.Model):
    slug = models.CharField(max_length=100)
    setting_name = models.TextField()
    setting_value = models.TextField()
    last_reported = models.DateTimeField()

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        default_permissions = ()
        db_table = 'workforce"."constance_summary'


# extensions
class ExtensionSummary(models.Model):
    tenant = models.CharField(db_index=True, max_length=200)
    name = models.CharField(unique=True, max_length=100)
    is_enabled = models.BooleanField(db_index=True)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        default_permissions = ()
        db_table = 'workforce"."extension_summary'


# featureflags
class FeatureFlagSummary(models.Model):
    tenant = models.CharField(db_index=True, max_length=200)
    name = models.CharField(unique=True, max_length=100)
    is_enabled = models.BooleanField(db_index=True)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        default_permissions = ()
        db_table = 'workforce"."featureflag_summary'

# metrics datapoint

# template change request
class TemplateChangeRequestSummary(models.Model):
    # fmt: off
    tenant = models.CharField(db_index=True, max_length=200)
    tcr_pk = models.PositiveIntegerField()
    created = models.DateTimeField()
    currency = models.CharField(max_length=3, null=True, blank=True)
    requested_changes = ArrayField(models.CharField(max_length=100), default=list, blank=True, verbose_name="Requested modifications")
    status = models.CharField(max_length=20, db_index=True)
    status_changed_requested = models.DateTimeField()
    status_changed_approved = models.DateTimeField()
    status_changed_completed = models.DateTimeField()
    template_key = models.CharField(max_length=200)
    template_name = models.CharField(max_length=200)
    template_content_type_model = models.CharField(max_length=200)
    estimated_price = models.PositiveIntegerField()
    estimated_hours = models.DecimalField(decimal_places=4, max_digits=11)
    # fmt: on

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        default_permissions = ()
        db_table = (
            'workforce"."templates_template_change_request_summary'
        )


# customer_all_users
class UserSummaryRow(models.Model):
    # fmt: off
    last_synced = models.DateTimeField(db_index=True)
    tenant = models.CharField(db_index=True, max_length=200)
    user_pk = models.PositiveIntegerField(db_index=True)
    email = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255)
    license = models.CharField(max_length=10, db_index=True)
    is_active = models.BooleanField(db_index=True)
    is_superuser = models.BooleanField(db_index=True)
    created = models.DateTimeField(db_index=True)
    last_access = models.DateTimeField(null=True, blank=True, db_index=True)
    groups = ArrayField(models.CharField(max_length=150), default=list, blank=True)
    # fmt: on

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        default_permissions = ()
        db_table = 'workforce"."customer_all_users'


# customer_onboarding_actions
class OnboardingActionRow(models.Model):
    # fmt: off
    tenant = models.CharField(db_index=True, max_length=200)
    last_synced = models.DateTimeField(db_index=True)
    is_active = models.BooleanField(db_index=True)

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    due_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    responsibility = models.CharField(max_length=100)
    assigned_to = models.CharField(max_length=100, blank=True, default='')
    progress = models.IntegerField(blank=True, null=True)
    effort = models.IntegerField(blank=True, null=True)
    group = models.CharField(max_length=100)
    # fmt: on

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        default_permissions = ()
        db_table = 'workforce"."customer_onboarding_actions'


class UsageMetrics(models.Model):
    tenant = models.CharField(db_index=True, max_length=200)
    count_name = models.CharField(db_index=True, max_length=200)
    stat_count = models.BigIntegerField()
    as_of = models.DateTimeField(db_index=True)

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'
        db_table = 'workforce"."usage_metrics'

        indexes =   [
            models.Index(fields=['tenant', 'count_name', '-as_of'], name='usage_metrics_latest_btree'),
        ]


class ServerUsage(models.Model):
    """Resource usage.

    This is an unmanaged model that lets us easily grab the resources used by the customer
    for the current billing cycle.

    TODO not sure where this belongs.
    """

    tenant = models.CharField(max_length=200, primary_key=True)
    staff_licenses_total = models.IntegerField()
    staff_licenses_used = models.IntegerField()  # This is all we're using currently
    staff_licenses_additional = models.IntegerField()
    desk_licenses_used = models.IntegerField()
    field_licenses_used = models.IntegerField()
    contractor_licenses_used = models.IntegerField()
    customer_licenses_used = models.IntegerField()
    api_licenses_used = models.IntegerField()
    reporting_licenses_used = models.IntegerField()
    timesheet_licenses_used = models.IntegerField()
    last_synced = models.DateTimeField()
    for_date = models.DateField()

    class Meta:
        managed = model_settings.DATAWAREHOUSE_MANAGED_MODELS
        app_label = 'workforce'

        default_permissions = ()
        db_table = 'workforce"."licensing_usage'