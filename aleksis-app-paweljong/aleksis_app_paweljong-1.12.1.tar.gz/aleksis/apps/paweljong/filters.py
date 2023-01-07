from django.utils.translation import gettext_lazy as _

from django_filters import FilterSet
from material import Layout, Row

from aleksis.core.filters import MultipleCharFilter

from .models import Event, EventRegistration, Terms, Voucher


class EventRegistrationFilter(FilterSet):
    person = MultipleCharFilter(
        [
            "person__first_name__icontains",
            "person__last_name__icontains",
        ],
        label=_("Search by name"),
    )

    class Meta:
        model = EventRegistration
        fields = ["states", "retracted"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.layout = Layout(
            Row("person", "states", "retracted"),
        )


class VoucherFilter(FilterSet):
    event = MultipleCharFilter(
        [
            "event__display_name__icontains",
        ],
        label=_("Search by event"),
    )

    name = MultipleCharFilter(
        [
            "person__first_name__icontains",
            "person__last_name__icontains",
        ],
        label=_("Search by name"),
    )

    class Meta:
        model = Voucher
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.layout = Layout(Row("event", "name"))


class TermsFilter(FilterSet):
    class Meta:
        model = Terms
        fields = ["title"]


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ["display_name", "published", "place"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.layout = Layout(
            Row("display_name"),
            Row("published", "place"),
        )
