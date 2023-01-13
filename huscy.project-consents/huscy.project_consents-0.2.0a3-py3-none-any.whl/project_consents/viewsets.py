from django.shortcuts import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import ProjectConsent, ProjectConsentCategory
from .serializer import ProjectConsentSerializer, ProjectConsentCategorySerializer
from huscy.projects.models import Project
from huscy.projects.permissions import IsProjectCoordinator


class ProjectConsentCategoryViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                    UpdateModelMixin, GenericViewSet):
    http_method_names = 'get', 'post', 'put', 'delete', 'head', 'options', 'trace'
    permission_classes = DjangoModelPermissions,
    queryset = ProjectConsentCategory.objects.all()
    serializer_class = ProjectConsentCategorySerializer


class ProjectConsentViewSet(ModelViewSet):
    permission_classes = IsAuthenticated, (DjangoModelPermissions | IsProjectCoordinator)
    serializer_class = ProjectConsentSerializer

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return ProjectConsent.objects.filter(project=self.project)

    def perform_create(self, serializer):
        serializer.save(project=self.project)
