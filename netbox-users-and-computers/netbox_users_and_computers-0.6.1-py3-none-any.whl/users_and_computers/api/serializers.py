from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Risk, RiskRelation#, RiskAssignment
from django.contrib.auth.models import ContentType
from drf_yasg.utils import swagger_serializer_method
from netbox.api.fields import ChoiceField, ContentTypeField
from utilities.api import get_serializer_for_model


class NestedRiskSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:users_and_computers-api:risk-detail'
    )

    class Meta:
        model = Risk
        fields = ('id', 'display', 'url', 'name', 'description')


class RiskSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:users_and_computers-api:risk-detail'
    )

    class Meta:
        model = Risk
        fields = ('id', 'url', 'display', 'name', 'description')


class NestedRiskRelationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:users_and_computers-api:riskrelation-detail'
    )

    class Meta:
        model = RiskRelation
        fields = ('id', 'url', 'display', 'name', 'description')


class RiskRelationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:users_and_computers-api:riskrelation-detail'
    )

    class Meta:
        model = RiskRelation
        fields = ('id', 'url', 'display', 'name', 'description')


