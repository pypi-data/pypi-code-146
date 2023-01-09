from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet

from .models import ProjectConsentCategory
from .serializer import ProjectConsentCategorySerializer


class ProjectConsentCategoryViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                    UpdateModelMixin, GenericViewSet):
    http_method_names = 'get', 'post', 'put', 'delete', 'head', 'options', 'trace'
    permission_classes = DjangoModelPermissions,
    queryset = ProjectConsentCategory.objects.all()
    serializer_class = ProjectConsentCategorySerializer
