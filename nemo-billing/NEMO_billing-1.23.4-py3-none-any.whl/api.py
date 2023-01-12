from NEMO.utilities import export_format_datetime
from drf_excel.mixins import XLSXFileMixin
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.fields import CharField
from rest_framework.viewsets import ReadOnlyModelViewSet

from NEMO_billing.models import CustomCharge


class CustomChargeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = CustomCharge
        fields = "__all__"
        expandable_fields = {
            "customer": "NEMO.serializers.UserSerializer",
            "creator": "NEMO.serializers.UserSerializer",
            "project": "NEMO.serializers.ProjectSerializer",
        }

    customer_name = CharField(source="customer.get_name")
    creator_name = CharField(source="creator.get_name")


class CustomChargeViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    queryset = CustomCharge.objects.all()
    serializer_class = CustomChargeSerializer
    filterset_fields = {
        "name": ["exact"],
        "customer": ["exact", "in"],
        "creator": ["exact", "in"],
        "project": ["exact", "in"],
        "date": ["exact", "month", "year", "gte", "gt", "lte", "lt"],
        "amount": ["exact", "gte", "gt", "lte", "lt"],
        "core_facility": ["exact", "in", "isnull"],
    }

    def get_filename(self, *args, **kwargs):
        return f"custom_charges-{export_format_datetime()}.xlsx"
