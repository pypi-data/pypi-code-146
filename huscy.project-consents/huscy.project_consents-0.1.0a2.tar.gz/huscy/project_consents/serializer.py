from rest_framework.serializers import ModelSerializer

from .models import ProjectConsentCategory


class ProjectConsentCategorySerializer(ModelSerializer):
    class Meta:
        model = ProjectConsentCategory
        fields = 'id', 'name', 'text_fragments'
