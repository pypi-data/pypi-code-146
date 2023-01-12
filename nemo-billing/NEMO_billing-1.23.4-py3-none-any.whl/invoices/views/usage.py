from logging import getLogger
from typing import List

from NEMO.decorators import accounting_or_user_office_or_manager_required
from NEMO.models import Account, Project, User
from NEMO.utilities import BasicDisplayTable, export_format_datetime, format_datetime
from NEMO.views.usage import date_parameters_dictionary, get_managed_projects, get_project_applications
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from NEMO_billing.invoices.invoice_data_processor import BillableItem
from NEMO_billing.invoices.invoice_generator import invoice_generator_class
from NEMO_billing.invoices.models import InvoiceConfiguration
from NEMO_billing.invoices.utilities import display_amount

logger = getLogger(__name__)


@login_required
@require_GET
def usage(request):
    user: User = request.user
    user_managed_projects = get_managed_projects(user)
    base_dictionary, start, end, kind, identifier = date_parameters_dictionary(request)
    customer_filter = Q(customer=user) | Q(project__in=user_managed_projects)
    user_filter = Q(user=user) | Q(project__in=user_managed_projects)
    trainee_filter = Q(trainee=user) | Q(project__in=user_managed_projects)
    project_id = request.GET.get("pi_project")
    csv_export = bool(request.GET.get("csv", False))
    if user_managed_projects:
        base_dictionary["selected_project"] = "all"
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        base_dictionary["selected_project"] = project
        customer_filter = customer_filter & Q(project=project)
        user_filter = user_filter & Q(project=project)
        trainee_filter = trainee_filter & Q(project=project)
    config = InvoiceConfiguration.first_or_default()
    detailed_items = sorted_billable_items(start, end, config, customer_filter, user_filter, trainee_filter)
    if csv_export:
        return csv_export_response(detailed_items)
    else:
        dictionary = {
            "detailed_items": detailed_items,
            "total_charges": display_amount(sum([item.amount for item in detailed_items if item.amount]), config),
            "can_export": True,
        }
        if user_managed_projects:
            dictionary["pi_projects"] = user_managed_projects
        dictionary["no_charges"] = not dictionary["detailed_items"]
        return render(request, "invoices/usage.html", {**base_dictionary, **dictionary})


@accounting_or_user_office_or_manager_required
@require_GET
def project_usage(request):
    base_dictionary, start, end, kind, identifier = date_parameters_dictionary(request)

    detailed_items: List[BillableItem] = []
    config = InvoiceConfiguration.first_or_default()

    projects = []
    user = None
    selection = ""
    try:
        if kind == "application":
            projects = Project.objects.filter(application_identifier=identifier)
            selection = identifier
        elif kind == "project":
            projects = [Project.objects.get(id=identifier)]
            selection = projects[0].name
        elif kind == "account":
            account = Account.objects.get(id=identifier)
            projects = Project.objects.filter(account=account)
            selection = account.name
        elif kind == "user":
            user = User.objects.get(id=identifier)
            projects = user.active_projects()
            selection = str(user)

        if projects:
            customer_filter = Q(project__in=projects)
            user_filter = Q(project__in=projects)
            trainee_filter = Q(project__in=projects)
            if user:
                customer_filter = customer_filter & Q(customer=user)
                user_filter = user_filter & Q(user=user)
                trainee_filter = trainee_filter & Q(trainee=user)
            detailed_items = sorted_billable_items(start, end, config, customer_filter, user_filter, trainee_filter)
            if bool(request.GET.get("csv", False)):
                return csv_export_response(detailed_items)
    except Exception as e:
        logger.error(e)
        pass
    dictionary = {
        "search_items": set(Account.objects.all())
        | set(Project.objects.all())
        | set(get_project_applications())
        | set(User.objects.filter(is_active=True)),
        "detailed_items": detailed_items,
        "total_charges": display_amount(sum([item.amount or 0 for item in detailed_items]), config),
        "project_autocomplete": True,
        "selection": selection,
        "can_export": True,
    }
    dictionary["no_charges"] = not dictionary["detailed_items"]
    return render(request, "invoices/usage.html", {**base_dictionary, **dictionary})


def sorted_billable_items(start, end, config, customer_filter, user_filter, trainee_filter) -> List[BillableItem]:
    data_processor = invoice_generator_class.get_invoice_data_processor()
    items = data_processor.get_billable_items(start, end, config, customer_filter, user_filter, trainee_filter, False)
    items.sort(key=lambda x: (-x.item_type.value, x.start), reverse=True)
    return items


def csv_export_response(detailed_items: List[BillableItem]):
    table_result = BasicDisplayTable()
    table_result.add_header(("type", "Type"))
    table_result.add_header(("user", "User"))
    table_result.add_header(("username", "Username"))
    table_result.add_header(("name", "Item"))
    table_result.add_header(("project", "Project"))
    table_result.add_header(("start", "Start time"))
    table_result.add_header(("end", "End time"))
    table_result.add_header(("quantity", "Quantity"))
    table_result.add_header(("rate", "Rate"))
    table_result.add_header(("cost", "Cost"))
    for billable_item in detailed_items:
        table_result.add_row(
            {
                "type": billable_item.item_type.display_name(),
                "user": billable_item.user.get_name(),
                "username": billable_item.user.username,
                "name": billable_item.name,
                "project": billable_item.project.name,
                "start": format_datetime(billable_item.start, "SHORT_DATETIME_FORMAT"),
                "end": format_datetime(billable_item.end, "SHORT_DATETIME_FORMAT"),
                "quantity": billable_item.quantity,
                "rate": billable_item.rate.display_rate() if billable_item.rate else "",
                "cost": round(billable_item.amount, 2) if billable_item.amount else "",
            }
        )
    response = table_result.to_csv()
    filename = f"usage_export_{export_format_datetime()}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
