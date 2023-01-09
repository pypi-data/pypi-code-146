from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField()

class SuccessSerializer(serializers.Serializer):
    status = serializers.CharField()