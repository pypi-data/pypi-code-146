from netbox.api.viewsets import NetBoxModelViewSet

from .. import models
from .serializers import RiskSerializer, RiskRelationSerializer, RiskAssignmentSerializer
from .. import filtersets


class RiskListViewSet(NetBoxModelViewSet):
    queryset = models.Risk.objects.prefetch_related('tags')
    serializer_class = RiskSerializer


class RiskRelationListViewSet(NetBoxModelViewSet):
    queryset = models.RiskRelation.objects.prefetch_related('tags')
    serializer_class = RiskRelationSerializer

