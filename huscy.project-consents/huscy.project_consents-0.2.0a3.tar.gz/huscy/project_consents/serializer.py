from rest_framework import serializers

from .models import ProjectConsent, ProjectConsentCategory
from .services import create_project_consent, update_project_consent
from huscy.consents.serializer import ConsentSerializer


class ProjectConsentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectConsentCategory
        fields = 'id', 'name', 'text_fragments'


class ProjectConsentSerializer(serializers.ModelSerializer):
    consent = ConsentSerializer(read_only=True)
    name = serializers.CharField(write_only=True)
    text_fragments = serializers.JSONField(write_only=True)

    class Meta:
        model = ProjectConsent
        fields = 'id', 'consent', 'name', 'project', 'text_fragments'
        read_only_fields = 'project',

    def create(self, validated_data):
        return create_project_consent(**validated_data)

    def update(self, project_consent, validated_data):
        return update_project_consent(project_consent, **validated_data)
