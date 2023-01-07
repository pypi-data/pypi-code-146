from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from base_system.models import ExtraGroup, ContentTypeCates, ContentTypeEx
from django.contrib.auth.models import Group
from functools import reduce


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

    class Meta:
        model = ContentTypeCates
        fields = "__all__"


class ContentTypeExSerializer(serializers.ModelSerializer):
    """
    功能菜单序列化扩展
    """

    class Meta:
        model = ContentTypeEx
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单／功能序列化
    """
    path = serializers.SerializerMethodField()
    # icon = serializers_folder.SerializerMethodField()
    class Meta:
        model = ContentTypeCates
        fields = "__all__"


    def get_path(self,obj):
        path=''
        if obj.content_cates.all():
            # print('bb',obj.content_cates.all().first())

            path=obj.content_cates.all().first().front_url
        return path

    def get_icon(self,obj):
        icon = obj.icon_class
        if obj.content_cates.all():
            # print('bb',obj.content_cates.all().first())

            icon = obj.content_cates.all().first().icon_class
        return icon

class GroupSerializer(serializers.ModelSerializer):
    """
    角色序列化
    """

    class Meta:
        model = Group
        fields = "__all__"


class GroupSerializerDetail(serializers.ModelSerializer):
    """
    角色序列化
    """
    permissions_serializer = serializers.SerializerMethodField()  # 当前角色所有权限
    # own_menu_tree = serializers_folder.SerializerMethodField()  # 当前角色权限树形结构
    # all_menu_tree = serializers_folder.SerializerMethodField()  # 所有权限树形结构

    class Meta:
        model = Group
        fields = "__all__"

    def get_content_types(self, obj, values=None):  # 获取content_type并去重
        if values:  # 所有权限
            content_type_ids = list(map(
                lambda perm: perm.content_type_id, Permission.objects.all()))
        else:  # 正常用户权限
            content_type_ids = list(map(
                lambda perm: perm.content_type_id, obj.permissions.all()))
        return ContentType.objects.filter(id__in=content_type_ids).distinct().all()

    def get_contentypecatrels(self, obj, values=None):
        # 获取所有的终极菜单
        content_types = self.get_content_types(obj, values)
        contentypeex = map(
            lambda ct: list(ct.extension.all()), content_types)
        try:
            content_type_cat_rels = reduce(lambda a, b: a + b, contentypeex)
            contentypecatrels = [a.content_type_cat for a in content_type_cat_rels]
        except Exception as e:
            contentypecatrels = []
        return contentypecatrels

    def get_parent(self, li, rels):
        if rels.parent:
            li.append(rels.parent)
            self.get_parent(li, rels.parent)
        return li

    def get_own_menu(self, obj, values=None):
        content_type_cat_rels = self.get_contentypecatrels(obj, values)
        rel_list = []
        for rel in content_type_cat_rels:
            self.get_parent(rel_list, rel)
        rel_list += content_type_cat_rels
        rel_list = list(set(rel_list))
        serializer_rels = ContentTypeCateSerializer(rel_list, many=True)
        return serializer_rels.data

    def get_menu_tree(self, obj, values=None):
        all_menu = self.get_own_menu(obj, values)
        menu_list = []
        for menu in all_menu:
            if not menu['parent']:
                menu_list.append(menu)
        for menu_1 in all_menu:
            children_list = []
            for children in all_menu:
                if children['parent'] == menu_1['id']:
                    children_list.append(children)
            menu_1['children'] = children_list
            if values:  # 获取所有菜单级权限,否则只获取菜单
                content_type_ex = ContentTypeEx.objects.filter(content_type_cat_id=menu_1['id']).first()
                if content_type_ex:
                    menu_1["permissions"]=map(lambda p: {"id": p.id, "name": p.name, "codename": p.codename},
                                               content_type_ex.content_type.permission_set.all())
        return menu_list

    def get_own_menu_tree(self, obj):
        menu_list = self.get_menu_tree(obj)
        return menu_list

    def get_all_menu_tree(self, obj):
        menu_list = self.get_menu_tree(obj, 1)
        return menu_list

    def get_permissions_serializer(self, obj):
        return PermissionSerializer(obj.permissions, many=True).data
