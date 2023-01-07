from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from base_system.models import ExtraGroup, ContentTypeCates, ContentTypeEx


class PermissionSerializer(serializers.ModelSerializer):
    """
    操作权限
    """

    class Meta:
        model = Permission
        fields = "__all__"


class ExtraGroupSerializer(serializers.ModelSerializer):
    """
    角色扩充序列化
    """

    class Meta:
        model = ExtraGroup
        fields = "__all__"


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    功能序列化
    """

    class Meta:
        model = ContentType
        fields = "__all__"


class ContentTypeCateSerializer(serializers.ModelSerializer):
    """
    菜单／功能序列化
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = ContentTypeCates
        fields = "__all__"

    def get_children(self,obj):
        content_type_ex = obj.content_cates
        serializer = ContentTypeExSerializer(content_type_ex, many=True)
        serializer_data = serializer.data
        return serializer_data


class ContentTypeExSerializer(serializers.ModelSerializer):
    """
    功能菜单序列化扩展
    """
    id = serializers.SerializerMethodField()

    class Meta:
        model = ContentTypeEx
        fields = "__all__"

    def get_id(self,obj):
        new_id = 'nn' + str(obj.id)
        return new_id


def get_parent(li, rels):
    if rels.parent:
        if rels.parent not in li:
            li.append(rels.parent)
            get_parent(li, rels.parent)
    return li


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单／功能序列化
    """
    id = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    # icon = serializers_folder.SerializerMethodField()

    class Meta:
        model = ContentTypeCates
        fields = "__all__"


    def get_id(self,obj):
        new_id = 'n' + str(obj.id)
        return new_id

    def get_path(self,obj):
        path=''
        if obj.content_cates.all():
            path=obj.content_cates.all().first().front_url
        return path

    def get_icon(self,obj):
        icon = obj.icon_class
        if obj.content_cates.all():
            icon = obj.content_cates.all().first().icon_class
        return icon
