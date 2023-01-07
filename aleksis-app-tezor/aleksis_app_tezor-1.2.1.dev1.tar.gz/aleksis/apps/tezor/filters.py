from django_filters import ChoiceFilter, FilterSet
from material import Layout, Row
from payments import PaymentStatus

from .models.invoice import Invoice


class InvoicesFilter(FilterSet):
    variant = ChoiceFilter(choices=Invoice.get_variant_choices())
    status = ChoiceFilter(choices=PaymentStatus.CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.layout = Layout(
            Row("variant", "status"),
        )

    class Meta:
        models = Invoice
