from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from NEMO.models import (
    AreaAccessRecord,
    ConsumableWithdraw,
    Project,
    Reservation,
    StaffCharge,
    TrainingSession,
    UsageEvent,
    User,
)
from NEMO.views.api_billing import get_minutes_between_dates
from django.conf import settings
from django.db.models import F, Q, QuerySet, Sum

from NEMO_billing.invoices.exceptions import (
    InvoiceItemsNotInFacilityException,
    NoProjectCategorySetException,
    NoRateSetException,
)
from NEMO_billing.invoices.models import (
    BillableItemType,
    Invoice,
    InvoiceConfiguration,
    InvoiceDetailItem,
    InvoiceSummaryItem,
)
from NEMO_billing.invoices.utilities import display_amount, flatten, name_for_billable_item
from NEMO_billing.models import CoreFacility, CustomCharge
from NEMO_billing.rates.models import Rate, RateCategory, RateType


class BillableItem(object):
    """ Object representing a billable item (Tool usage, area access, consumable etc.) """

    def __init__(self, item, project: Project, configuration: InvoiceConfiguration = None):
        self.item = item
        self.project: Optional[Project] = project
        self.configuration = configuration or InvoiceConfiguration()
        # Actual items
        self.tool = None
        self.area = None
        self.consumable = None
        # Rate (to be set later)
        self.rate: Optional[Rate] = None
        # Other properties
        self.start = getattr(item, "start", None) or getattr(item, "date", None)
        self.end = getattr(item, "end", None) or getattr(item, "date", None)
        self.user = getattr(item, "user", None) or getattr(item, "customer", None) or getattr(item, "trainee", None)
        self.proxy_user = (
            getattr(item, "operator", None)
            or getattr(item, "staff_member", None)
            or getattr(item, "creator", None)
            or getattr(item, "merchant", None)
            or getattr(item, "trainer", None)
            or getattr(getattr(item, "staff_charge", None), "staff_member", None)
        )
        # Setting tool, area, consumable and other properties
        self.item_type: Optional[BillableItemType] = None
        # Set quantity and amount if we know they cannot change later (Custom charge or supplies or training duration etc.)
        self.quantity: Optional[Decimal] = None
        self.amount: Optional[Decimal] = None
        self.core_facility: Optional[CoreFacility] = None
        self.rate_type: Optional[RateType] = None
        if isinstance(item, UsageEvent):
            self.tool = item.tool
            self.rate_type = RateType.objects.get(type=RateType.Type.TOOL_USAGE)
            # Usage event by staff on behalf of user is considered staff charge
            usage_by_staff = item.operator != item.user and item.operator.is_staff
            self.item_type = BillableItemType.TOOL_USAGE
            if usage_by_staff and settings.STAFF_TOOL_USAGE_AS_STAFF_CHARGE:
                self.item_type = BillableItemType.STAFF_CHARGE
        elif isinstance(item, AreaAccessRecord):
            self.area = item.area
            self.rate_type = RateType.objects.get(type=RateType.Type.AREA_USAGE)
            # Area access during staff charge is considered staff charge
            self.item_type = BillableItemType.AREA_ACCESS
            staff_charge = item.staff_charge
            if staff_charge and settings.STAFF_AREA_ACCESS_AS_STAFF_CHARGE:
                self.item_type = BillableItemType.STAFF_CHARGE
        elif isinstance(item, StaffCharge):
            self.item_type = BillableItemType.STAFF_CHARGE
            self.rate_type = RateType.objects.get(type=RateType.Type.STAFF_CHARGE)
            if not getattr(item, "core_facility", None):
                # We first check if there was an area access, in which case we will use the area's facility
                area_charge: AreaAccessRecord = AreaAccessRecord.objects.filter(staff_charge_id=item.id).first()
                if area_charge:
                    self.core_facility = area_charge.area.core_facility
                else:
                    # Otherwise, check for tool usage on behalf of the same customer during the time
                    tool_usage: UsageEvent = UsageEvent.objects.filter(
                        operator=item.staff_member, user=item.customer, start__gt=item.start, start__lte=item.end
                    ).first()
                    if tool_usage:
                        self.core_facility = tool_usage.tool.core_facility
        elif isinstance(item, Reservation):
            self.item_type = BillableItemType.MISSED_RESERVATION
            self.tool = item.tool
            self.area = item.area
            if self.tool:
                self.rate_type = RateType.objects.get(type=RateType.Type.TOOL_MISSED_RESERVATION)
            if self.area:
                self.rate_type = RateType.objects.get(type=RateType.Type.AREA_MISSED_RESERVATION)
        elif isinstance(item, CustomCharge):
            self.item_type = BillableItemType.CUSTOM_CHARGE
            # Quantity and amount will never change so set them now
            self.quantity = 1
            self.amount = item.amount
        elif isinstance(item, TrainingSession):
            self.item_type = BillableItemType.TRAINING
            self.tool = item.tool
            # Training duration will never change
            self.quantity = item.duration
            if item.type == TrainingSession.Type.INDIVIDUAL:
                self.rate_type = RateType.objects.get(type=RateType.Type.TOOL_TRAINING_INDIVIDUAL)
            else:
                self.rate_type = RateType.objects.get(type=RateType.Type.TOOL_TRAINING_GROUP)
        elif isinstance(item, ConsumableWithdraw):
            self.item_type = BillableItemType.CONSUMABLE
            self.consumable = item.consumable
            # Supply order quantity will never change
            self.quantity = item.quantity
            self.rate_type = RateType.objects.get(type=RateType.Type.CONSUMABLE)
        if not self.core_facility:
            self.core_facility = (
                getattr(item, "core_facility", None)
                or getattr(self.tool, "core_facility", None)
                or getattr(self.area, "core_facility", None)
                or getattr(self.consumable, "core_facility", None)
            )

    @property
    def name(self):
        return name_for_billable_item(self)

    @property
    def display_rate(self):
        return get_rate_with_currency(self.configuration, self.rate.display_rate()) if self.rate else None

    @property
    def display_amount(self):
        return display_amount(self.amount, self.configuration)

    @property
    def rate_time_name_add(self):
        return f" - {self.rate.time.name}" if self.rate and self.rate.time else ""

    def copy_and_calculate_amount(self, rate, new_start, new_end):
        new_billable = deepcopy(self)
        new_billable.rate = rate
        new_billable.start = new_start
        new_billable.end = new_end
        # Calculate quantity only if it wasn't already set
        if not new_billable.quantity:
            new_billable.quantity = get_minutes_between_dates(new_billable.start, new_billable.end)
        # Calculate amount only if not already set
        if not new_billable.amount:
            new_billable.amount = rate.calculate_amount(new_billable.quantity)
        return new_billable


def find_rates(rate_type: RateType, project: Project, tool=None, area=None, consumable=None) -> List[Rate]:
    kwargs = {"type_id": rate_type.id}
    if rate_type.category_specific:
        if RateCategory.objects.exists() and not project.projectbillingdetails.category:
            raise NoProjectCategorySetException(rate_type, project)
        kwargs["category"] = project.projectbillingdetails.category
    if rate_type.item_specific:
        if tool:
            kwargs["tool_id"] = tool.id
        elif area:
            kwargs["area_id"] = area.id
        elif consumable:
            kwargs["consumable_id"] = consumable.id
    if not rate_type.can_have_rate_time():
        # We can only have one rate, so we can use the .get() function
        try:
            return [Rate.non_deleted().get(**kwargs)]
        except Rate.DoesNotExist:
            raise NoRateSetException(rate_type, kwargs.get("category"), tool=tool, area=area, consumable=consumable)
    else:
        # Use filter to get all rates
        rates = Rate.non_deleted().filter(**kwargs)
        # We need at least one rate, and one of them being a base rate (without time)
        if not rates or not any([rate for rate in rates if not rate.time]):
            raise NoRateSetException(rate_type, kwargs.get("category"), tool=tool, area=area, consumable=consumable)
        return rates


def get_rate_with_currency(config: InvoiceConfiguration, rate: str):
    return f"{config.currency} {rate}" if config.currency else rate


class InvoiceDataProcessor(object):
    tool_usage_staff_filter = Q(operator__is_staff=True) & ~Q(operator=F("user"))

    def process_data(self, start, end, project_details, configuration, user: User) -> Optional[Invoice]:
        invoice = self.create_invoice(start, end, project_details, configuration, user)
        project_filter = Q(project_id=project_details.project_id)
        billables = self.get_billable_items(start, end, configuration, project_filter, project_filter, project_filter)
        detail_items: List[InvoiceDetailItem] = list(map(billable_to_invoice_detail_item, billables))
        if settings.INVOICE_ALL_ITEMS_MUST_BE_IN_FACILITY:
            for detail_item in detail_items:
                if not detail_item.core_facility:
                    raise InvoiceItemsNotInFacilityException(detail_item)
        if detail_items:
            invoice.save()
            for detail_item in detail_items:
                detail_item.invoice = invoice
                detail_item.save(force_insert=True)
            self.add_invoice_summary_items(invoice)
            return invoice

    def get_billable_items(
        self, start, end, config, customer_filter=Q(), user_filter=Q(), trainee_filter=Q(), raise_no_rate=True
    ) -> List[BillableItem]:
        items: List[BillableItem] = []
        items.extend(self.area_access_records_details(start, end, config, customer_filter, raise_no_rate))
        items.extend(self.consumable_withdrawals_details(start, end, config, customer_filter, raise_no_rate))
        items.extend(self.missed_reservations_details(start, end, config, user_filter, raise_no_rate))
        items.extend(self.staff_charges_details(start, end, config, customer_filter, raise_no_rate))
        items.extend(self.training_sessions_details(start, end, config, trainee_filter, raise_no_rate))
        items.extend(self.tool_usages_details(start, end, config, user_filter, raise_no_rate))
        items.extend(self.custom_charges_details(start, end, config, customer_filter, raise_no_rate))
        return items

    def create_invoice(self, start, end, project_details, configuration, user: User) -> Invoice:
        invoice = Invoice()
        invoice.start = start
        invoice.end = end
        invoice.project_details = project_details
        invoice.configuration = configuration
        invoice.created_by = user
        invoice.total_amount = 0
        return invoice

    def tool_usages_details(self, start, end, config, x_filter=Q(), raise_no_rate=True) -> List[BillableItem]:
        usage_events = UsageEvent.objects.filter(end__gte=start, end__lte=end)
        usage_events = usage_events.filter(x_filter).order_by("start")
        return flatten([process_billables(u, u.project, config, raise_no_rate) for u in usage_events])

    def area_access_records_details(self, start, end, config, x_filter=Q(), raise_no_rate=True) -> List[BillableItem]:
        access_records = AreaAccessRecord.objects.filter(end__gte=start, end__lte=end)
        access_records = access_records.filter(x_filter).order_by("start")
        return flatten([process_billables(access, access.project, config, raise_no_rate) for access in access_records])

    def missed_reservations_details(self, start, end, config, x_filter=Q(), raise_no_rate=True) -> List[BillableItem]:
        missed_res = Reservation.objects.filter(missed=True, end__gte=start, end__lte=end)
        missed_res = missed_res.filter(x_filter).order_by("start")
        return flatten([process_billables(missed, missed.project, config, raise_no_rate) for missed in missed_res])

    def staff_charges_details(self, start, end, config, x_filter=Q(), raise_no_rate=True) -> List[BillableItem]:
        staff_charges = StaffCharge.objects.filter(end__gte=start, end__lte=end)
        staff_charges = staff_charges.filter(x_filter).order_by("start")
        return flatten([process_billables(c, c.project, config, raise_no_rate) for c in staff_charges])

    def consumable_withdrawals_details(self, start, end, config, x_filter=Q(), raise_no_rate=True) -> List[BillableItem]:
        withdrawals = ConsumableWithdraw.objects.filter(date__gte=start, date__lte=end)
        withdrawals = withdrawals.filter(x_filter).order_by("date")
        return flatten([process_billables(w, w.project, config, raise_no_rate) for w in withdrawals])

    def training_sessions_details(self, start, end, config, x_filter=Q(), raise_no_rate=True) -> List[BillableItem]:
        training_sessions = TrainingSession.objects.filter(date__gte=start, date__lte=end)
        training_sessions = training_sessions.filter(x_filter).order_by("date")
        return flatten([process_billables(t, t.project, config, raise_no_rate) for t in training_sessions])

    def custom_charges_details(self, start, end, config, x_filter=Q(), raise_no_rate=True) -> List[BillableItem]:
        custom_charges = CustomCharge.objects.filter(date__gte=start, date__lte=end)
        custom_charges = custom_charges.filter(x_filter).order_by("date")
        return flatten([process_billables(cc, cc.project, config, raise_no_rate) for cc in custom_charges])

    def add_invoice_summary_items(self, invoice):
        # Core facilities sorted alphabetically by non empty ones first
        for core_facility in invoice.sorted_core_facilities():
            self._add_summary_items_for_facility(invoice, core_facility)

        # Recap of all charges
        charges_amount = invoice.invoicesummaryitem_set.filter(
            summary_item_type=InvoiceSummaryItem.InvoiceSummaryItemType.SUBTOTAL
        ).aggregate(Sum("amount"))["amount__sum"]

        # Tax
        tax_amount = Decimal(0)
        if invoice.configuration.tax and charges_amount > Decimal(0) and not invoice.project_details.no_tax:
            tax = InvoiceSummaryItem(
                invoice=invoice, name=f"{invoice.configuration.tax_name} ({invoice.configuration.tax_display()}%)"
            )
            tax.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.TAX
            tax_amount = charges_amount * invoice.configuration.tax_amount()
            tax.amount = tax_amount
            tax.save(force_insert=True)

        invoice.total_amount = charges_amount + tax_amount
        invoice.save(update_fields=["total_amount"])

    def _add_summary_items_for_facility(self, invoice: Invoice, core_facility: Optional[str]):
        details = invoice.invoicedetailitem_set.filter(core_facility=core_facility)
        self._add_aggregate_items_with_details(invoice, core_facility, details, BillableItemType.TOOL_USAGE)
        self._add_aggregate_items_with_details(invoice, core_facility, details, BillableItemType.AREA_ACCESS)
        self._add_aggregate_items_with_details(invoice, core_facility, details, BillableItemType.CONSUMABLE)
        self._add_aggregate_items_with_details(invoice, core_facility, details, BillableItemType.STAFF_CHARGE)
        self._add_aggregate_items_with_details(invoice, core_facility, details, BillableItemType.TRAINING)
        self._add_aggregate_items_with_details(invoice, core_facility, details, BillableItemType.MISSED_RESERVATION)
        self._add_aggregate_items_with_details(invoice, core_facility, details, BillableItemType.CUSTOM_CHARGE)

        facility_subtotal = InvoiceSummaryItem(invoice=invoice, name="Subtotal", core_facility=core_facility)
        facility_subtotal.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.SUBTOTAL
        facility_subtotal.amount = details.aggregate(Sum("amount"))["amount__sum"]
        facility_subtotal.save(force_insert=True)

    def _add_aggregate_items_with_details(
        self, invoice, core_facility: str, items: QuerySet, item_type: BillableItemType
    ):
        items = items.filter(item_type=item_type.value)
        if items.exists():
            item_names = list(items.values_list("name", flat=True).distinct())
            item_names.sort()
            for item_name in item_names:
                item_name_qs = items.filter(name=item_name)
                item_rate: Rate = item_name_qs.first().rate
                total_q = item_name_qs.aggregate(Sum("quantity"))["quantity__sum"]
                if item_type.is_time_type():
                    quantity_display = f" ({total_q/60:.2f} hours)"
                elif item_type == BillableItemType.CUSTOM_CHARGE:
                    quantity_display = ""
                else:
                    quantity_display = f" (x {total_q})"
                summary_item_name = f"{item_name}{quantity_display}"
                summary_item = InvoiceSummaryItem(invoice=invoice, name=summary_item_name, core_facility=core_facility)
                summary_item.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.ITEM
                summary_item.item_type = item_type.value
                summary_item.details = item_rate
                summary_item.amount = item_name_qs.aggregate(Sum("amount"))["amount__sum"]
                summary_item.save(force_insert=True)

    def category_name_for_item_type(self, item_type: Optional[Union[BillableItemType, int]]) -> str:
        billable_item_type = (
            item_type
            if isinstance(item_type, BillableItemType)
            else BillableItemType(item_type)
            if isinstance(item_type, int)
            else None
        )
        if not billable_item_type:
            return ""
        if billable_item_type == BillableItemType.TOOL_USAGE:
            return "Tool Usage"
        elif billable_item_type == BillableItemType.AREA_ACCESS:
            return "Area Access"
        elif billable_item_type == BillableItemType.CONSUMABLE:
            return "Supplies/Materials"
        elif billable_item_type == BillableItemType.STAFF_CHARGE:
            return "Technical Work"
        elif billable_item_type == BillableItemType.TRAINING:
            return "Training"
        elif billable_item_type == BillableItemType.MISSED_RESERVATION:
            return "Missed Reservations"
        elif billable_item_type == BillableItemType.CUSTOM_CHARGE:
            return "Other"

    def name_for_item(self, billable_item: BillableItem) -> str:
        name = (
            getattr(billable_item.tool, "name", None)
            or getattr(billable_item.area, "name", None)
            or getattr(billable_item.consumable, "name", None)
            or getattr(billable_item.item, "name", None)
        )
        if isinstance(billable_item.item, TrainingSession):
            name = f"{billable_item.tool.name} ({billable_item.item.get_type_display()})"
        if not name and isinstance(billable_item.item, StaffCharge):
            name = "Staff time"
        return f"{name}{billable_item.rate_time_name_add}"


def billable_to_invoice_detail_item(item: BillableItem) -> InvoiceDetailItem:
    invoice_item = InvoiceDetailItem()
    invoice_item.content_object = item.item
    invoice_item.quantity = item.quantity
    invoice_item.start = item.start
    invoice_item.end = item.end
    invoice_item.user = item.user.username if item.user else None
    invoice_item.amount = item.amount
    invoice_item.rate = item.display_rate
    invoice_item.core_facility = item.core_facility
    invoice_item.item_type = item.item_type.value
    invoice_item.name = item.name
    return invoice_item


def process_billables(item, project, configuration: InvoiceConfiguration, raise_no_rate=True) -> List[BillableItem]:
    billable = BillableItem(item, project, configuration)
    try:
        # Only proceed if we don't have an amount already
        if not billable.amount:
            # Otherwise, find the rates and calculate the amount
            rates = find_rates(billable.rate_type, billable.project, billable.tool, billable.area, billable.consumable)
            billables: List[BillableItem] = []
            break_up_and_add(billables, rates, billable.start, billable.end, billable)
            return billables
    except (NoRateSetException, NoProjectCategorySetException):
        if raise_no_rate:
            raise
    # If we already have an amount, or if there is an error and we don't raise it, return the original billable
    return [billable]


def break_up_and_add(billables, rates: List[Rate], start_time: datetime, end_time: datetime, original_billable):
    # This function will break the date range into chunks of BillableItems if there are multiple rates that apply
    # 1. Find the earliest rate that applies to this date range as well as its start time and end time.
    # 2. The new start is the one given by the first_rate_that_applies method (max of rate start time and original start time)
    # 3. If the new start is later than the start, that means we have a gap and need to apply the base rate to the in between times
    # 4. The new end is the min of rate start time + rate duration and the original end
    # 5. Apply it to a new BillableItem and calculate the new amount.
    # 6. Call recursively on the rest of the date range (new end until original end)
    # 7. Recursion ends when we don't have a rate with time that applies (set base rate and done)
    rate, new_start, new_end = earliest_rate_match(rates, start_time, end_time)
    base_rate = next(r for r in rates if not r.time)
    if not rate:
        billables.append(original_billable.copy_and_calculate_amount(base_rate, start_time, end_time))
    else:
        # If the new start is later than the current start, we have a "hole" between timed rates, so apply the original base rate
        if new_start > start_time:
            billables.append(original_billable.copy_and_calculate_amount(base_rate, start_time, new_start))
        billables.append(original_billable.copy_and_calculate_amount(rate, new_start, new_end))
        # keep going until we reach the end
        if new_end != end_time:
            break_up_and_add(billables, rates, new_end, end_time, original_billable)


def earliest_rate_match(rates: List[Rate], start_time: datetime, end_time: datetime) -> (Rate, datetime, datetime):
    new_rate, new_start, new_end = None, None, None
    for rate in rates:
        # We only care about rate with times, since they are the only ones that can override the base rate
        if rate.time:
            tmp_start, tmp_end = rate.time.earliest_match(start_time, end_time)
            if tmp_start and (not new_start or tmp_start < new_start):
                new_start = tmp_start
                new_end = tmp_end
                new_rate = rate
    return new_rate, new_start, new_end
