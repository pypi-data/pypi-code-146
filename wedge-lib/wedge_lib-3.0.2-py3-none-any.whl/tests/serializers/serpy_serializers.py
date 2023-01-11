from w.drf.serializers.serpy_serializers import UserSerializer
from w.serializers import serializer


class RequestResponseSerializer(serializer.SerpySerializer):
    content = serializer.Field()
    success = serializer.Field()
    status_code = serializer.Field()
    redirect_location = serializer.Field()


class MailOutboxSerializer(serializer.SerpySerializer):
    to = serializer.Field()
    bcc = serializer.Field()
    cc = serializer.Field()
    from_email = serializer.Field()
    reply_to = serializer.Field()
    subject = serializer.Field()
    body = serializer.Field()
    content_subtype = serializer.Field()


class UserSsoNoAuthUserTestSerializer(serializer.SerpySerializer):
    sso_uuid = serializer.Field()
    list_apps = serializer.Field()


class UserSsoTestSerializer(UserSsoNoAuthUserTestSerializer):
    user = UserSerializer()


class UserWithSsoUserTestSerializer(UserSerializer):
    sso_user = UserSsoNoAuthUserTestSerializer()
