from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A


class ManageEventsTable(tables.Table):
    class Meta:
        attrs = {"class": "responsive-table highlight"}

    display_name = tables.Column(verbose_name=_("Event"))
    date_event = tables.Column(verbose_name=_("Date"))
    max_participants = tables.Column(verbose_name=_("Max. participants"))
    date_registration = tables.Column(verbose_name=_("Registration until"))

    edit = tables.LinkColumn(
        "edit_event_by_slug",
        args=[A("slug")],
        verbose_name=_("Edit"),
        text=_("Edit"),
    )

    view_public = tables.LinkColumn(
        "event_by_name",
        args=[A("slug")],
        verbose_name=_("Public page"),
        text=_("Public page"),
    )

    view = tables.LinkColumn(
        "event_detail_by_name",
        args=[A("slug")],
        verbose_name=_("View"),
        text=_("View"),
    )


class VouchersTable(tables.Table):
    class Meta:
        attrs = {"class": "responsive-table highlight"}

    event = tables.Column(verbose_name=_("Event"))
    discount = tables.Column(verbose_name=_("Amount"))
    code = tables.Column(verbose_name=_("Code"))
    person = tables.Column(verbose_name=_("Person"))
    deleted = tables.LinkColumn(
        "delete_voucher_by_pk",
        args=[A("id")],
        verbose_name=_("Delete"),
        text=_("Delete"),
    )
    edit = tables.LinkColumn(
        "edit_voucher_by_pk", args=[A("id")], verbose_name=_("Edit"), text=_("Edit")
    )
    print_voucher = tables.LinkColumn(
        "print_voucher_by_pk", args=[A("id")], verbose_name=_("Print"), text=_("Print")
    )


class EventRegistrationsTable(tables.Table):
    class Meta:
        attrs = {"class": "responsive-table highlight"}

    person = tables.Column()
    states = tables.Column()
    checked_in_date = tables.Column()
    retracted = tables.Column()
    view = tables.LinkColumn(
        "registration_by_pk",
        args=[A("id")],
        verbose_name=_("View registration"),
        text=_("View"),
    )
    check_in = tables.LinkColumn(
        "check_in_registration_by_pk",
        args=[A("pk")],
        verbose_name=_("Check in"),
        text=_("Check in"),
    )
    edit = tables.LinkColumn(
        "edit_registration_by_pk",
        args=[A("pk")],
        verbose_name=_("Edit"),
        text=_("Edit"),
    )

    def render_states(self, value, record):
        context = dict(states=value.all())
        return render_to_string("paweljong/registration_state/chip.html", context)


class TermsTable(tables.Table):
    class Meta:
        attrs = {"class": "responsive-table highlight"}

    title = tables.Column()

    edit = tables.LinkColumn(
        "edit_term_by_pk",
        args=[A("id")],
        verbose_name=_("Edit"),
        text=_("Edit"),
    )


class InfoMailingsTable(tables.Table):
    class Meta:
        attrs = {"class": "responsive-table highlight"}

    subject = tables.Column()

    edit = tables.LinkColumn(
        "edit_info_mailing_by_pk",
        args=[A("id")],
        verbose_name=_("Edit"),
        text=_("Edit"),
    )
    delete = tables.LinkColumn(
        "delete_info_mailing_by_pk",
        args=[A("id")],
        verbose_name=_("Delete"),
        text=_("Delete"),
    )


class RegistrationStatesTable(tables.Table):
    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.Column()

    edit = tables.LinkColumn(
        "edit_registration_state_by_pk",
        args=[A("id")],
        verbose_name=_("Edit"),
        text=_("Edit"),
    )

    def render_name(self, value, record):
        context = dict(state=record)
        return render_to_string("paweljong/registration_state/chip.html", context)


class ChildGroupsTable(tables.Table):
    """Table to list groups."""

    class Meta:
        attrs = {"class": "highlight"}

    name = tables.LinkColumn("group_by_id", args=[A("id")])
    short_name = tables.LinkColumn("group_by_id", args=[A("id")])

    add_persons = tables.LinkColumn(
        "add_persons_to_group",
        args=[A("id")],
        verbose_name=_("Add persons"),
        text=_("Add persons"),
    )


class AdditionalFieldsTable(tables.Table):
    class Meta:
        attrs = {"class": "highlight"}

    title = tables.LinkColumn("edit_additional_field_by_id", args=[A("id")])
