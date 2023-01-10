from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from .models import Consent
from .serializer import ConsentSerializer


class ConsentViewSet(ModelViewSet):
    permission_classes = DjangoModelPermissions,
    queryset = Consent.objects.all()
    serializer_class = ConsentSerializer
