from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A

from aleksis.core.util.tables import SelectColumn


class PurchasedItemsTable(tables.Table):
    sku = tables.Column(verbose_name=_("Art. No."))
    name = tables.Column(verbose_name=_("Item"), attrs={"td": {"class": "hero-col"}})
    tax_rate = tables.TemplateColumn(
        verbose_name=_("Tax Rate"),
        template_code="{{value}} %",
        attrs={"td": {"class": "right-align"}},
    )
    quantity = tables.Column(verbose_name=_("Qty."), attrs={"td": {"class": "right-align"}})
    price = tables.TemplateColumn(
        verbose_name=_("Net"),
        template_code="{{value|floatformat:2}} {{record.currency}}",
        attrs={"td": {"class": "right-align"}},
    )

    class Meta:
        orderable = False


class TotalsTable(tables.Table):
    name = tables.Column(attrs={"td": {"class": "right-align hero-col"}})
    value = tables.TemplateColumn(
        template_code="{{value|floatformat:2}} {{record.currency}}",
        attrs={"td": {"class": "right-align"}},
    )

    class Meta:
        show_header = False
        orderable = False


class ClientsTable(tables.Table):
    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.Column()

    view = tables.LinkColumn(
        "client_by_pk",
        args=[A("id")],
        verbose_name=_("View"),
        text=_("View"),
    )
    edit = tables.LinkColumn(
        "edit_client_by_pk",
        args=[A("id")],
        verbose_name=_("Edit"),
        text=_("Edit"),
    )
    delete = tables.LinkColumn(
        "delete_client_by_pk",
        args=[A("id")],
        verbose_name=_("Delete"),
        text=_("Delete"),
    )


class InvoiceGroupsTable(tables.Table):

    name = tables.Column()
    template_name = tables.Column()
    view = tables.LinkColumn(
        "invoice_group_by_pk",
        args=[A("id")],
        verbose_name=_("View"),
        text=_("View"),
    )
    edit = tables.LinkColumn(
        "edit_invoice_group_by_pk",
        args=[A("id")],
        verbose_name=_("Edit"),
        text=_("Edit"),
    )
    delete = tables.LinkColumn(
        "delete_invoice_group_by_pk",
        args=[A("id")],
        verbose_name=_("Delete"),
        text=_("Delete"),
    )


class InvoicesTable(tables.Table):
    selected = SelectColumn()

    number = tables.Column()
    status = tables.Column()
    created = tables.DateColumn()
    billing_first_name = tables.Column()
    billing_last_name = tables.Column()
    total = tables.Column()
    view = tables.LinkColumn(
        "invoice_by_token",
        args=[A("token")],
        verbose_name=_("View"),
        text=_("View"),
    )
    print = tables.LinkColumn(
        "print_invoice",
        args=[A("token")],
        verbose_name=_("Print"),
        text=_("Print"),
    )

    class Meta:
        attrs = {"class": "highlight"}
