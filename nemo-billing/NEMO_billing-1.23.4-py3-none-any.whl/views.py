from http import HTTPStatus

from NEMO.decorators import (
    accounting_or_user_office_or_manager_required,
    any_staff_required,
    staff_member_required,
    synchronized,
)
from NEMO.exceptions import ProjectChargeException
from NEMO.models import AreaAccessRecord, Project, StaffCharge, Tool, UsageEvent, User
from NEMO.views.get_projects import get_projects
from NEMO.views.pagination import SortedPaginator
from NEMO.views.policy import check_billing_to_project, check_policy_to_enable_tool
from NEMO.views.staff_charges import staff_charges
from NEMO.views.tool_control import interlock_bypass_allowed, interlock_error
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from NEMO_billing.admin import CustomChargeAdminForm, save_or_delete_core_facility
from NEMO_billing.models import CoreFacility, CustomCharge


@accounting_or_user_office_or_manager_required
@require_http_methods(["GET", "POST"])
def custom_charges(request):
    page = SortedPaginator(CustomCharge.objects.all(), request, order_by="-date").get_current_page()
    core_facilities_exist = CoreFacility.objects.exists()
    return render(
        request, "billing/custom_charges.html", {"page": page, "core_facilities_exist": core_facilities_exist}
    )


@accounting_or_user_office_or_manager_required
@require_http_methods(["GET", "POST"])
def create_or_modify_custom_charge(request, custom_charge_id=None):
    custom_charge = None
    try:
        custom_charge = CustomCharge.objects.get(id=custom_charge_id)
    except CustomCharge.DoesNotExist:
        pass

    form = CustomChargeAdminForm(request.POST or None, instance=custom_charge)

    dictionary = {
        "core_facilities": CoreFacility.objects.all(),
        "core_facility_required": settings.CUSTOM_CHARGE_CORE_FACILITY_REQUIRED,
        "form": form,
        "users": User.objects.filter(is_active=True),
    }
    if request.method == "POST" and form.is_valid():
        charge: CustomCharge = form.save()
        message = f'Your custom charge "{charge.name}" of {charge.amount} for {charge.customer} was successfully logged and will be billed to project {charge.project}.'
        messages.success(request, message=message)
        return redirect("custom_charges")
    else:
        if custom_charge:
            dictionary["projects"] = custom_charge.customer.active_projects()
        if hasattr(form, "cleaned_data") and "customer" in form.cleaned_data:
            dictionary["projects"] = form.cleaned_data["customer"].active_projects()
        return render(request, "billing/custom_charge.html", dictionary)


# Overriding begin staff charge
@staff_member_required
@require_GET
def custom_staff_charges(request):
    staff_member: User = request.user
    staff_charge: StaffCharge = staff_member.get_staff_charge()
    dictionary = dict()
    error = None
    customer = None
    try:
        customer = User.objects.get(id=request.GET["customer"])
    except:
        pass
    if staff_charge:
        return staff_charges(request)
    if customer:
        if customer.active_project_count() > 0:
            dictionary["customer"] = customer
            dictionary["core_facility_id"] = request.GET.get("core_facility")
            if not settings.STAFF_CHARGE_CORE_FACILITY_REQUIRED or dictionary["core_facility_id"]:
                return render(request, "staff_charges/choose_project.html", dictionary)
            else:
                error = "you must select a core facility"
        else:
            error = str(customer) + " does not have any active projects. You cannot bill staff time to this user."
    dictionary["users"] = User.objects.filter(is_active=True).exclude(id=request.user.id)
    dictionary["core_facilities"] = CoreFacility.objects.all()
    dictionary["core_facility_required"] = settings.STAFF_CHARGE_CORE_FACILITY_REQUIRED
    dictionary["error"] = error
    return render(request, "staff_charges/new_custom_staff_charge.html", dictionary)


@staff_member_required
@require_POST
def custom_begin_staff_charge(request):
    if request.user.charging_staff_time():
        return HttpResponseBadRequest("You cannot create a new staff charge when one is already in progress.")
    charge = StaffCharge()
    charge.customer = User.objects.get(id=request.POST["customer"])
    charge.project = Project.objects.get(id=request.POST["project"])
    core_facility = None
    try:
        core_facility = CoreFacility.objects.get(id=request.POST["core_facility"])
    except:
        pass
    if settings.STAFF_CHARGE_CORE_FACILITY_REQUIRED and not core_facility:
        return HttpResponseBadRequest("You cannot create a new staff charge without a core facility.")
    # Check if we are allowed to bill to project
    try:
        check_billing_to_project(charge.project, charge.customer, charge)
    except ProjectChargeException as e:
        return HttpResponseBadRequest(e.msg)
    charge.staff_member = request.user
    charge.save()
    if core_facility:
        save_or_delete_core_facility(charge, core_facility, "staff_charge")
    return redirect(reverse("staff_charges"))


# Overriding enable tool
@login_required
@require_POST
@synchronized("tool_id")
def custom_enable_tool(request, tool_id, user_id, project_id, staff_charge):
    if not settings.ALLOW_CONDITIONAL_URLS:
        return HttpResponseBadRequest(
            "Tool control is only available on campus. We're working to change that! Thanks for your patience."
        )

    tool = get_object_or_404(Tool, id=tool_id)
    operator = request.user
    user = get_object_or_404(User, id=user_id)
    project = get_object_or_404(Project, id=project_id)
    staff_charge = staff_charge == "true"
    bypass_interlock = request.POST.get("bypass", "False") == "True"
    response = check_policy_to_enable_tool(tool, operator, user, project, staff_charge)
    if response.status_code != HTTPStatus.OK:
        return response

    # All policy checks passed so enable the tool for the user.
    if tool.interlock and not tool.interlock.unlock():
        if bypass_interlock and interlock_bypass_allowed(user):
            pass
        else:
            return interlock_error("Enable", user)

    # Start staff charge before tool usage
    if staff_charge:
        new_staff_charge = StaffCharge()
        new_staff_charge.staff_member = request.user
        new_staff_charge.customer = user
        new_staff_charge.project = project
        new_staff_charge.save()
        if tool.core_facility:
            save_or_delete_core_facility(new_staff_charge, tool.core_facility, "staff_charge")
        # If the tool requires area access, start charging area access time
        if tool.requires_area_access:
            area_access = AreaAccessRecord()
            area_access.area = tool.requires_area_access
            area_access.staff_charge = new_staff_charge
            area_access.customer = new_staff_charge.customer
            area_access.project = new_staff_charge.project
            area_access.save()

    # Create a new usage event to track how long the user uses the tool.
    new_usage_event = UsageEvent()
    new_usage_event.operator = operator
    new_usage_event.user = user
    new_usage_event.project = project
    new_usage_event.tool = tool
    new_usage_event.save()

    return response


@any_staff_required
@require_GET
def get_projects_for_custom_charges(request):
    return get_projects(request)
