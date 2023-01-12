from typing import List, Tuple

from NEMO.models import Area, Consumable, Tool
from NEMO.utilities import distinct_qs_value_list
from NEMO.views.pagination import SortedPaginator
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET, require_http_methods

from NEMO_billing.decorators import accounting_or_manager_required
from NEMO_billing.rates.admin import RateAdminForm
from NEMO_billing.rates.customization import BillingRatesCustomization
from NEMO_billing.rates.models import Rate, RateCategory, RateTime, RateType


@accounting_or_manager_required
@require_GET
def rates(request, rate_type_choice: str = None):
    rate_type = rate_type_choice or RateType.Type.TOOL
    rate_types = get_rate_types(rate_type)
    rate_order_by = [rate_type.lower(), "type", "category", "time"]
    if rate_type_choice and rate_type_choice.lower() == "other":
        rate_types = RateType.objects.filter(item_specific=False)
        rate_order_by = []
    rate_qs = Rate.non_deleted()
    page_qs = rate_qs.filter(type__in=rate_types).order_by(*rate_order_by)
    page = SortedPaginator(page_qs, request, order_by="type" if not rate_order_by else None).get_current_page()
    # remove when fixed in NEMO (allowing no order_type)
    if rate_order_by:
        page.paginator.order_by = ""

    # Creating rates list for search autocomplete
    rate_search = "["
    for tool_id in distinct_qs_value_list(rate_qs.filter(tool__isnull=False), "tool"):
        tool = Tool.objects.get(pk=tool_id)
        rate_search += '{{"name":"{0}", "id":{1}, "type_value": "{2}"}},'.format(
            escape(tool.name), tool_id, RateType.Type.TOOL
        )
    for area_id in distinct_qs_value_list(rate_qs.filter(area__isnull=False), "area"):
        area = Area.objects.get(pk=area_id)
        rate_search += '{{"name":"{0}", "id":{1}, "type_value": "{2}"}},'.format(
            escape(area.name), area_id, RateType.Type.AREA
        )
    for consumable_id in distinct_qs_value_list(rate_qs.filter(consumable__isnull=False), "consumable"):
        consumable = Consumable.objects.get(pk=consumable_id)
        rate_search += '{{"name":"{0}", "id":{1}, "type_value": "{2}"}},'.format(
            escape(consumable.name), consumable_id, RateType.Type.CONSUMABLE
        )
    for rate_type_item in RateType.objects.all():
        if not rate_type_item.item_specific:
            if rate_qs.filter(type=rate_type_item).exists():
                rate_search += '{{"name":"{0}", "id":"{1}", "type_value": "{2}"}},'.format(
                    escape(str(rate_type_item)), "", rate_type_item.get_rate_group_type()
                )
    rate_search = rate_search.rstrip(",") + "]"
    rate_search = mark_safe(rate_search)

    dictionary = {
        "rate_type": rate_type,
        "page": page,
        "show_type": page_qs.values("type").distinct().count() > 1 or rate_type.lower() == "other",
        "show_category": page_qs.filter(category__isnull=False).exists(),
        "show_time": page_qs.filter(time__isnull=False).exists(),
        "search_rates": rate_search,
    }

    return render(request, "rates/rates.html", dictionary)


@accounting_or_manager_required
@require_http_methods(["GET", "POST"])
def create_or_modify_rate(request, rate_type_choice=None, item_id=None):
    tool = get_object_or_404(Tool, pk=item_id) if item_id and rate_type_choice == RateType.Type.TOOL else None
    area = get_object_or_404(Area, pk=item_id) if item_id and rate_type_choice == RateType.Type.AREA else None
    consumable = (
        get_object_or_404(Consumable, pk=item_id) if item_id and rate_type_choice == RateType.Type.CONSUMABLE else None
    )

    # Add children tools here too, they should be able to have a rate even though they are not visible
    tools = list(Tool.objects.filter(Q(visible=True) | Q(parent_tool__isnull=False)))
    # Because we are showing tool children, we cannot sort the queryset (child tool has no category)
    tools.sort(key=lambda x: (x.category, x.name))
    rate_types = get_rate_types(rate_type_choice)

    dictionary = {
        "rate_types": rate_types,
        "rate_type_choice": rate_type_choice,
        "item": tool or area or consumable,
        "rate_type_choices": get_rate_type_choices(),
        "rate_categories": RateCategory.objects.all(),
        "rate_times": RateTime.objects.all(),
        "tools": tools,
        "areas": Area.objects.filter(area_children_set__isnull=True),
        "consumables": Consumable.objects.all().order_by("category", "name"),
    }

    if request.method == "GET":
        rate_forms = get_forms(request, rate_types, tool, area, consumable)
    else:
        rate_forms = post_forms(request)
        # We do a first pass to check that all forms are valid

        forms_to_validate = rate_forms
        forms_to_delete = []
        allow_blank_rates = BillingRatesCustomization.get("allow_blank_rate") == "enabled"
        if allow_blank_rates:
            forms_to_validate = [form for form in rate_forms if form.has_rate_amount()]
            forms_to_delete = [form for form in rate_forms if not form.has_rate_amount() and form.instance.id]
        all_forms_valid = all([form.is_valid() for form in forms_to_validate]) if forms_to_validate else False
        if all_forms_valid:
            for rate_form in forms_to_validate:
                # We have to check the form validity each time we save a rate, in case the next one breaks uniqueness for example
                rate_form.full_clean()
                if not rate_form.is_valid():
                    dictionary["forms"] = rate_forms
                    return render(request, "rates/rate.html", dictionary)
                # Don't commit since we want to save it using our own method
                form_rate: Rate = rate_form.save(commit=False)
                form_rate.save_with_user(request.user)
                rate_form.save_m2m()
            for rate_form_delete in forms_to_delete:
                rate_form_delete.instance.delete()
            message = f"Your rates were successfully saved."
            messages.success(request, message=message)
            return redirect("rates")

    dictionary["forms"] = rate_forms
    return render(request, "rates/rate.html", dictionary)


# We are building forms for each rate type, for each category.
# The goal is to have all rate forms related to one group type (Tool, Area, Supply etc.) in one view.
def get_forms(request, rate_types: List[RateType], tool, area, consumable) -> List[RateAdminForm]:
    forms = []
    categories = RateCategory.objects.all()
    missed_reservation_flat = getattr(settings, "DEFAULT_MISSED_RESERVATION_FLAT", True)
    # Create a form for each rate type
    count = 0
    for rate_type in rate_types:
        missed_r_type = rate_type.type in [RateType.Type.TOOL_MISSED_RESERVATION, RateType.Type.AREA_MISSED_RESERVATION]
        default_flat = missed_r_type and missed_reservation_flat or rate_type.type == RateType.Type.CONSUMABLE
        if rate_type.category_specific and categories:
            # Add a form for each category
            for category in categories:
                count, n_forms = init_forms(request, count, rate_type, default_flat, tool, area, consumable, category)
                forms.extend(n_forms)
        else:
            count, n_forms = init_forms(request, count, rate_type, default_flat, tool, area, consumable)
            forms.extend(n_forms)
    return forms


def init_forms(request, count, rate_type, flat, tool=None, area=None, consumable=None, category=None):
    forms = []
    previous_rates = Rate.non_deleted().filter(type=rate_type, category=category, tool=tool, area=area, consumable=consumable)
    if previous_rates.exists():
        for prev_rate in previous_rates:
            count = count + 1
            forms.append(RateAdminForm(form_number=count, instance=prev_rate))
    else:
        count = count + 1
        instance = Rate(type=rate_type, category=category, tool=tool, area=area, consumable=consumable, flat=flat)
        forms.append(RateAdminForm(form_number=count, instance=instance))
    return count, forms


def post_forms(request) -> List[RateAdminForm]:
    forms = []
    form_numbers: List[str] = request.POST.getlist("form_numbers[]")
    for form_number in form_numbers:
        data = {}
        for field in ["type", "category", "time", "tool", "area", "consumable", "amount", "flat", "minimum_charge"]:
            data[field] = request.POST.get(form_number + "_" + field)
        rate_id = request.POST.get(form_number + "_id")
        instance = Rate.objects.get(pk=rate_id) if rate_id else None
        forms.append(RateAdminForm(form_number=form_number, data=data, instance=instance))
    return forms


def get_rate_type_choices() -> List[Tuple[str, str]]:
    # Since we want to group all tool related types, we only have a subset here
    # Return a list of (value, display value) for use in a select
    rate_type_choices = set()
    for rate_type in RateType.objects.all():
        if rate_type.is_tool_rate() and rate_type.item_specific:
            rate_type_choices.add((RateType.Type.TOOL, RateType.Type.TOOL))
        elif rate_type.is_area_rate() and rate_type.item_specific:
            rate_type_choices.add((RateType.Type.AREA, RateType.Type.AREA))
        elif rate_type.is_consumable_rate() and rate_type.item_specific:
            rate_type_choices.add((rate_type.type, rate_type.get_type_display()))
        else:
            rate_type_choices.add((rate_type.type, rate_type.get_type_display()))
    return sorted(rate_type_choices)


def get_rate_types(rate_type_choice: str) -> List[RateType]:
    rate_types = []
    if rate_type_choice:
        if rate_type_choice == RateType.Type.TOOL:
            rate_types = RateType.objects.filter(
                type__in=[
                    RateType.Type.TOOL_USAGE,
                    RateType.Type.TOOL_MISSED_RESERVATION,
                    RateType.Type.TOOL_TRAINING_INDIVIDUAL,
                    RateType.Type.TOOL_TRAINING_GROUP,
                ],
                item_specific=True,
            )
        elif rate_type_choice == RateType.Type.AREA:
            rate_types = RateType.objects.filter(
                type__in=[RateType.Type.AREA_USAGE, RateType.Type.AREA_MISSED_RESERVATION], item_specific=True
            )
        elif rate_type_choice == RateType.Type.CONSUMABLE:
            rate_types = RateType.objects.filter(type=RateType.Type.CONSUMABLE)
        else:
            rate_types = RateType.objects.filter(type=rate_type_choice)
    return rate_types


@accounting_or_manager_required
@require_GET
def new_time_rate_form(request):
    rate_type = get_object_or_404(RateType, pk=int(request.GET["type"]))
    category_id = request.GET.get("category", None) or None
    tool_id = request.GET.get("tool", None) or None
    area_id = request.GET.get("area", None) or None
    consumable_id = request.GET.get("consumable", None) or None
    count = request.GET["count"]
    missed_reservation_flat = getattr(settings, "DEFAULT_MISSED_RESERVATION_FLAT", True)
    missed_r_type = rate_type.type in [RateType.Type.TOOL_MISSED_RESERVATION, RateType.Type.AREA_MISSED_RESERVATION]
    default_flat = missed_r_type and missed_reservation_flat or rate_type.type == RateType.Type.CONSUMABLE
    instance = Rate(
        type=rate_type,
        category_id=category_id,
        tool_id=tool_id,
        area_id=area_id,
        consumable_id=consumable_id,
        flat=default_flat,
    )
    rate_form = RateAdminForm(form_number=count, instance=instance)
    dictionary = {"rate_form": rate_form, "show_rate_time": True, "rate_times": RateTime.objects.all()}
    return render(request, "rates/rate_form_details.html", dictionary)


@accounting_or_manager_required
@require_GET
def delete_rate_time(request, rate_id):
    rate = get_object_or_404(Rate, pk=rate_id)
    if not rate.time:
        return HttpResponseBadRequest("You can only delete rates with time")
    rate.delete_with_user(request.user)
    return HttpResponse()
