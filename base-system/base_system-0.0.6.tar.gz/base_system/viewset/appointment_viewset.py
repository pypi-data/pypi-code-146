from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import django_filters as filters

from base_system.appointment_ser import *
from base_system.models import Hospital, Office, Doctor


class HospitalFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    codenum = filters.CharFilter(field_name="codenum", lookup_expr='icontains')
    parent = filters.CharFilter(field_name="parent")

    class Meta:
        model = Hospital
        fields = (
            "name",
            "codenum",
            "parent",
        )


class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.filter(is_active=True).order_by('id')
    serializer_class = HospitalSerializer
    filterset_class = HospitalFilter
    # filter_fields = "__all__"


class OfficeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    codenum = filters.CharFilter(field_name="codenum", lookup_expr='icontains')
    office_type = filters.CharFilter(field_name="office_type", lookup_expr='icontains')
    hospital = filters.CharFilter(field_name="hospital")
    parent = filters.CharFilter(field_name="parent")

    class Meta:
        model = Office
        fields = "__all__"


class OfficeViewSet(ModelViewSet):
    queryset = Office.objects.filter(is_active=True)
    serializer_class = OfficeSerializer
    filter_fields = "__all__"
    # filterset_class = OfficeFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'page' in self.request.query_params.keys():
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorSerializer
    filter_fields = (
            "id",
            "name",
            "phone",
            "email",
            "address",
            "job_number",
            "position",
            "doc_rank",
            "gender",
            "nation",
            "idnum",
            "office",
            "hospital",
            "birthday",
            "describe",
            "is_online_consult",
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = None
        if 'page' in self.request.query_params.keys():
            page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if 'fee_type' in self.request.query_params.keys():
            fee_type = self.request.query_params.get('fee_type')
            serializer = self.get_serializer(queryset, many=True, context={'fee_type': fee_type})
            return Response({'results': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'fee_type' in self.request.query_params.keys():
            fee_type = self.request.query_params.get('fee_type')
            serializer = self.get_serializer(instance, context={'fee_type': fee_type})
            return Response(serializer.data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
