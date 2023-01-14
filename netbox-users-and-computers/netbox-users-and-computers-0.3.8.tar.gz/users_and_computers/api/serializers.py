"""
from rest_framework.serializers import ModelSerializer

from users_and_computers.models import MyModel1


class MyModel1Serializer(ModelSerializer):

    class Meta:
        model = MyModel1
        fields = '__all__'
"""
