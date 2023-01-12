from datetime import datetime
from typing import List

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import register
from django.db.models import Q
from django.forms import BaseInlineFormSet
from django.urls import reverse
from django.utils.safestring import mark_safe

from NEMO_billing.rates.models import DailySchedule, Rate, RateCategory, RateLog, RateTime, RateType


class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        """Check that at least one item has been entered."""
        super().clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get("DELETE", False) for cleaned_data in self.cleaned_data):
            raise forms.ValidationError("A minimum of one item is required.")


def delete_rates_with_message(request, rates: List[Rate], message=None):
    if rates:
        for rate in rates:
            delete_message = f"{rate} was deleted"
            if message:
                delete_message += f" ({message})"
            messages.warning(request, delete_message)
            rate.delete_with_user(request.user)


@register(RateCategory)
class RateCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # On add of first category, delete all category specific rates without a category
        delete_rates_with_message(
            request,
            Rate.non_deleted().filter(type__category_specific=True, category__isnull=True),
            "rate is category specific but had no category",
        )


@register(RateType)
class RateTypeAdmin(admin.ModelAdmin):
    list_display = ("type", "category_specific", "item_specific")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("type",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        old_rate_type = None
        if obj.pk:
            old_rate_type = RateType.objects.get(pk=obj.pk)
        super().save_model(request, obj, form, change)
        if old_rate_type:
            categories_exists = RateCategory.objects.exists()
            rate_qs = Rate.non_deleted()
            # Not category specific becomes category specific: delete old matching rates with no category (unless no Categories exist)
            if categories_exists and not old_rate_type.category_specific and obj.category_specific:
                delete_rates_with_message(
                    request,
                    rate_qs.filter(type=obj, category__isnull=True),
                    "had no category and rate type is now category specific",
                )
            # Not item specific becomes item specific: delete old matching rates with no item
            if not old_rate_type.item_specific and obj.item_specific:
                delete_rates_with_message(
                    request,
                    rate_qs.filter(type=obj, tool__isnull=True, area__isnull=True, consumable__isnull=True),
                    "had no item and rate type is now item specific",
                )
            # Category specific becomes not category specific: delete old matching rates with categories
            if old_rate_type.category_specific and not obj.category_specific:
                delete_rates_with_message(
                    request,
                    rate_qs.filter(type=obj, category__isnull=False),
                    "had a category and rate type is now non-category specific",
                )
            # Item specific becomes not item specific: delete old matching rates with items
            if old_rate_type.item_specific and not obj.item_specific:
                delete_rates_with_message(
                    request,
                    rate_qs.filter(type=obj).filter(
                        Q(tool__isnull=False) | Q(area__isnull=False) | Q(consumable__isnull=False)
                    ),
                    "had an item and rate type is now non-item specific",
                )


class RateAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.form_number = kwargs.pop("form_number", None)
        super().__init__(*args, **kwargs)

    def display_title(self):
        return f"{self.instance.type}{self.instance.display_category_time()}"

    def has_rate_amount(self):
        self.full_clean()
        amount_field = self.cleaned_data.get("amount")
        return amount_field == 0 or amount_field

    class Meta:
        model = Rate
        fields = "__all__"


class DailyScheduleAdminFormset(AtLeastOneRequiredInlineFormSet):
    def clean(self):
        # check that there is no overlap between each of the schedules in this formset
        super().clean()
        if any(self.errors):
            return
        if len(self.forms) > 1:
            previous_schedules = []
            control_datetime = datetime.today()
            for form in self.forms:
                if self.can_delete and self._should_delete_form(form) or not form.cleaned_data:
                    continue
                schedule = DailySchedule(
                    start_time=form.cleaned_data.get("start_time"),
                    end_time=form.cleaned_data.get("end_time"),
                    weekday=form.cleaned_data.get("weekday"),
                )
                for previous_schedule in previous_schedules:
                    if previous_schedule.overlaps(control_datetime, schedule):
                        raise forms.ValidationError(f"{previous_schedule} overlaps with {schedule}")
                previous_schedules.append(schedule)


class DailyScheduleAdminInline(admin.TabularInline):
    model = DailySchedule
    formset = DailyScheduleAdminFormset
    min_num = 1
    extra = 0


class RateTimeAdminForm(forms.ModelForm):
    class Meta:
        model = RateTime
        fields = "__all__"


@register(RateTime)
class RateTimeAdmin(admin.ModelAdmin):
    form = RateTimeAdminForm
    inlines = (DailyScheduleAdminInline,)
    list_display = ("name", "get_schedules_display")

    def get_schedules_display(self, rate_time: RateTime) -> str:
        return mark_safe("<br>".join([str(schedule) for schedule in DailySchedule.objects.filter(rate_time=rate_time)]))

    get_schedules_display.short_description = "Schedule"


@register(Rate)
class RateAdmin(admin.ModelAdmin):
    form = RateAdminForm
    list_display = ("get_item", "type", "category", "time", "amount", "flat", "minimum_charge")
    list_filter = ("type", "category", "time", "flat", "tool", "area", "consumable", "deleted")

    def get_queryset(self, request):
        # All of this to only show non-deleted rates
        try:
            # We have to match only the rate list URL since this queryset function is used to also edit etc.
            rates_url = reverse("admin:rates_rate_changelist")
            if request.path.endswith(rates_url):
                deleted_in_request = (
                    request and request.GET and any([param for param in request.GET if "deleted" in param.lower()])
                )
                if not deleted_in_request:
                    return super().get_queryset(request).filter(deleted=False)
        except:
            pass
        return super().get_queryset(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "type":
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj: Rate, form, change):
        obj.save_with_user(request.user)

    def delete_model(self, request, obj: Rate):
        obj.delete_with_user(request.user)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)


@register(RateLog)
class RateLogAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "user", "date", "get_content_object_display")
    list_filter = ["action"]
    date_hierarchy = "date"

    @admin.display(description="Item", ordering="content_type")
    def get_content_object_display(self, rate_log: RateLog):
        content_object = rate_log.content_object
        if not content_object:
            content_object = "Staff Charge"
        return content_object

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
