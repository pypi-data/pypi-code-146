from rest_framework.serializers import ModelSerializer

from .models import Consent
from .services import create_consent, update_consent


class ConsentSerializer(ModelSerializer):
    class Meta:
        model = Consent
        fields = 'id', 'name', 'text_fragments'

    def create(self, validated_data):
        return create_consent(**validated_data)

    def update(self, consent, validated_data):
        return update_consent(consent, **validated_data)
