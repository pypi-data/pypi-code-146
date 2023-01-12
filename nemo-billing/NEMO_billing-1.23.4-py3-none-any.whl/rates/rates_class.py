from itertools import groupby
from typing import Dict, Iterable, List

from NEMO.models import Consumable, Tool
from NEMO.rates import Rates
from NEMO.utilities import distinct_qs_value_list
from django.conf import settings
from django.utils.formats import number_format

from NEMO_billing.invoices.invoice_data_processor import get_rate_with_currency
from NEMO_billing.invoices.models import InvoiceConfiguration
from NEMO_billing.rates.models import Rate, RateCategory


class DatabaseRates(Rates):

    expand_rates_table = False

    def __init__(self):
        self.currency = getattr(settings, "RATE_CURRENCY", "$")
        self.configuration = InvoiceConfiguration.first_or_default()

    def load_rates(self, force_reload=False):
        super().load_rates(force_reload=force_reload)

    def get_consumable_rates(self, consumables: List[Consumable]) -> Dict[str, str]:
        return {
            rate.consumable.name: self.consumable_rate_display(rate)
            for rate in Rate.non_deleted().filter(consumable__in=consumables)
        }

    def get_consumable_rate(self, consumable: Consumable) -> str:
        consumable_rate = Rate.non_deleted().get(consumable=consumable)
        if consumable_rate.exists():
            return self.consumable_rate_display(consumable_rate)

    def get_tool_rate(self, tool: Tool) -> str:
        all_tool_rates = Rate.non_deleted().filter(tool=tool).order_by("type", "category")
        if not all_tool_rates:
            return ""
        list_by_type = groupby(all_tool_rates, key=lambda x: x.type)
        rate_categories = distinct_qs_value_list(all_tool_rates, "category")
        rate_categories = sorted([RateCategory.objects.get(id=cat_id).name for cat_id in rate_categories if cat_id])
        html_rate = f'<div class="media"><a onclick="toggle_details(this)" class="pointer collapsed" data-toggle="collapse" data-target="#rates_details"><span class="glyphicon glyphicon-list-alt pull-left notification-icon primary-highlight"></span><span class="glyphicon pull-left chevron glyphicon-chevron-{"down" if self.get_expand_rates_table() else "right"}"></span></a>'
        html_rate += f'<div class="media-body"><span class="media-heading">Rates</span><div id="rates_details" class="collapse {"in" if self.get_expand_rates_table() else ""}"><table class="table table-bordered table-hover thead-light" style="width: auto !important; margin-bottom: 0">'
        if rate_categories:
            html_rate += '<tr><th class="text-center"></th><th class="text-center">'
            html_rate += '</th><th class="text-center">'.join(rate_categories)
            html_rate += "</tr>"
        for rate_type, tool_rates in list_by_type:
            html_rate += (
                f'<tr><th class="text-center" style="vertical-align: middle">{rate_type.get_type_display()}</th>'
            )
            if not rate_type.category_specific or not RateCategory.objects.exists():
                html_rate += f'<td class="text-center" style="vertical-align: middle" colspan="{len(rate_categories)}">{self.tool_rate_display_with_details(tool_rates)}</td>'
            else:
                for rate_category in rate_categories:
                    tool_rate_category = all_tool_rates.filter(type=rate_type, category__name=rate_category)
                    html_rate += f'<td class="text-center" style="vertical-align: middle">{self.tool_rate_display_with_details(tool_rate_category)}</td>'
        html_rate += "</tr></table></div></div></div>"
        return html_rate

    def tool_rate_display_with_details(self, rates: Iterable[Rate]):
        return "<br>".join(
            [
                f"{get_rate_with_currency(self.configuration, rate.display_rate())}{' (' + rate.time.name + ')' if rate.time else ''}"
                for rate in rates
            ]
        )

    def consumable_rate_display(self, rate: Rate) -> str:
        return f"<b>{self.display_amount(rate.amount)}</b>"

    def display_amount(self, amount):
        return f"{self.currency}{number_format(amount, decimal_pos=2)}"
