from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from base_system.models import ExtraGroup, ContentTypeCates, ContentTypeEx, User, Hospital
from base_system.serializers_folder.group_serializers import GroupSerializer, ExtraGroupSerializer, ContentTypeCateSerializer, \
    ContentTypeExSerializer, MenuSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_fields = "__all__"
    # filterset_class = UserfFilter

    def get_parent(self, li, rels):
        if rels.parent:
            li.append(rels.parent)
            self.get_parent(li, rels.parent)
        return li

    @action(methods=["GET"], detail=True)
    def get_group_permission(self, request, pk):
        obj = self.get_object()
        # 获取当前组所拥有的权限
        permissions = Permission.objects.filter(group=obj.id).all().order_by('content_type_id')
        # serializer = PermissionSerializer(permissions, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)
        data = self.serializer_permission(permissions)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def get_all_permission(self, request):
        # 获取所有的权限
        permissions = Permission.objects.all().order_by('content_type_id')
        # serializer = PermissionSerializer(permissions, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)
        data = self.serializer_permission(permissions)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def get_ct_permission(self, request):
        # 获取当前组所拥有的权限
        ctrels = ContentTypeEx.objects.all().order_by('content_type_id')

        ret = map(
            lambda ctrel: {
                "id": ctrel.id,
                "name": ctrel.name,
                "permissions": map(
                    lambda p: {
                        "id": p.id,
                        "name": p.name,
                        "codename": p.codename
                    },
                    ctrel.content_type.permission_set.all()
                )
            },
            ctrels
        )

        # serializer = PermissionSerializer(permissions, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)

        # data = self.serializer_permission(permissions)
        return Response(data=ret, status=status.HTTP_200_OK)

    def serializer_permission(self, permissions):
        # 通过权限来得到权限的分类及权限的序列化信息
        permissions = set(permissions)
        content_types = map(lambda p: p.content_type, permissions)
        content_types = list(set(content_types))  # 得到去重的列表
        return map(
            lambda ct: {
                "id": ct.id,
                "name": ct.model,
                "permissions": map(
                    lambda p: {"id": p.id, "name": p.name, "codename": p.codename},
                    set(ct.permission_set.all()) & permissions
                )
            },
            content_types
        )

    # def retrieve(self, request, *args, **kwargs):
    #     # 获取单个角色的基本信息，该角色的权限，以及所有的权限
    #     obj = self.get_object()
    #     serializer = self.get_serializer(obj)
    #     # 基本的角色信息
    #     data = serializer.data
    #     # 该角色所拥有的权限
    #     permissions = Permission.objects.filter(group=obj.id).all().order_by('content_type_id')
    #     # serializer = PermissionSerializer(permissions, many=True)
    #     # data["permissions"] = serializer.data
    #     data["self_permissions"] = self.serializer_permission(permissions)
    #     # 所有的权限提供给修改使用
    #     total_permissions = Permission.objects.all().order_by('content_type_id')
    #     # serializer = PermissionSerializer(total_permissions, many=True)
    #     # data["total_permissions"] = serializer.data
    #     data["total_permissions"] = self.serializer_permission(total_permissions)
    #     return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        extra, group_data = self.check_data(request.data)
        # 创建角色及相关及权限
        new_group = Group.objects.filter(name=group_data["name"])
        if new_group:
            return Response(data={"msg": "角色已经存在"}, status=210)
        group = Group.objects.create(name=group_data["name"])
        group.permissions.set(group_data["permission_ids"])
        group.save()
        # 创建用户附加信息
        # extra = ExtraGroup.objects.create(group_id=group.pk, **extra)
        extra['group']=group.pk

        serializer = ExtraGroupSerializer(data=extra)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=GroupSerializer(group).data, status=status.HTTP_201_CREATED)

    def check_data(self, data):
        # 校验角色额外信息数据
        extra = dict()
        # data = dict(data)
        extra["note"] = data.get("note")
        extra["is_active"] = data.get("is_active", 1)
        extra["hospital"] = data.get("hospital_id")
        extra["order_by"] = data.get("order_by")
        extra["created_user"] = data.get("created_user")
        extra["role_code"] = data.get("role_code")
        serializer = ExtraGroupSerializer(data=extra)
        serializer.is_valid(raise_exception=True)
        extra = serializer.data

        # 校验角色数据
        group_data = dict()
        permissions = data.get("permission_ids")
        # group_data["permission_ids"] = eval(permissions) if permissions else None
        group_data["permission_ids"] = permissions if permissions else []
        if data.get("name"):
            group_data["name"] = data.get("name")
            serializer = GroupSerializer(data=group_data)
            serializer.is_valid(raise_exception=True)
            # group_data = serializer.data

        return extra, group_data

    def update(self, request, *args, **kwargs):
        group = self.get_object()
        extra_group = group.extra_group
        if request.data.get("name") == group.name:
            del request.data["name"]
        extra, group_data = self.check_data(request.data)
        extra_group.note = extra["note"]
        extra_group.is_active = extra["is_active"]
        extra_group.index = extra["order_by"]
        extra_group.hospital_id = extra["hospital"]
        extra_group.created_user = extra["created_user"]
        extra_group.role_code = extra["role_code"]
        extra_group.save()
        group.name = group_data.get('name', group.name)
        # if group_data.get("permission_ids"):
        group.permissions.set(group_data["permission_ids"])
        group.save()
        return Response(data=GroupSerializer(group).data, status=status.HTTP_205_RESET_CONTENT)

    # def destroy(self, request, *args, **kwargs):
    #     group = self.get_object()
    #     group.extra_group.is_active = 0
    #     group.extra_group.save()
    #     return Response(data={"message": "删除成功"}, status=status.HTTP_204_NO_CONTENT)


class ExtraGroupViewSet(ModelViewSet):
    queryset = ExtraGroup.objects.all()
    serializer_class = ExtraGroupSerializer
    filter_fields = "__all__"


class ContentTypeCatesViewSet(ModelViewSet):
    queryset = ContentTypeCates.objects.all()
    serializer_class = ContentTypeCateSerializer
    pagination_class = None
    filter_fields = "__all__"


class ContentTypeExViewSet(ModelViewSet):
    queryset = ContentTypeEx.objects.all()
    serializer_class = ContentTypeExSerializer
    filter_fields = "__all__"


def get_parent(li, rels):
    if rels.parent:
        if rels.parent not in li:
            li.append(rels.parent)
            get_parent(li, rels.parent)
    return li


def get_permissions(serializer,permissions,value):
    content_type_ids = list(map(lambda perm: perm.content_type_id, permissions))
    content_types = ContentType.objects.filter(id__in=content_type_ids).distinct().all()
    content_type_ex = ContentTypeEx.objects.filter(is_active=True,content_type_id__in=content_type_ids)
    content_type_cat_ids = list(map(lambda cat: cat.content_type_cat_id, content_type_ex))
    # print(content_type_cat_ids)
    content_type_cats = ContentTypeCates.objects.filter(id__in=content_type_cat_ids).order_by('order_by')
    rel_list = []
    for rel in content_type_cats:
        get_parent(rel_list, rel)
    rel_list += content_type_cats
    rel_list = list(set(rel_list))
    serializer_rels = serializer(rel_list, many=True)
    all_menu = serializer_rels.data
    menu_list = [menu for menu in all_menu if not menu['parent']]
    # for menu in all_menu:
    #     if not menu['parent']:
    #         menu_list.append(menu)
    for menu_1 in all_menu:
        children_list = [children for children in all_menu if children['parent'] == menu_1['id']]
        # for children in all_menu:
        #     if children['parent'] == menu_1['id']:
        #         children_list.append(children)
        children_list = sorted(children_list, key=lambda x: x['order_by'])
        menu_1['children'] = children_list
        content_type_ex = ContentTypeEx.objects.filter(content_type_cat_id=menu_1['id']).first()
        if value:
            if content_type_ex:
                menu_1["permissions"] = list(map(lambda p: {"id": p.id, "name": p.name, "codename": p.codename},
                                                 content_type_ex.content_type.permission_set.all()))
    menu_list = sorted(menu_list, key=lambda x: x['order_by'])
    return menu_list

def get_own_permissions(request):
    user_id=request.GET.get('user_id')
    user=User.objects.get(id=request.GET.get('user_id'))
    # defaultgroup = user.get_default_group
    # print(defaultgroup)
    # permissions = Permission.objects.filter(group=defaultgroup)

    allgroups = user.get_allgroups
    permissions = Permission.objects.filter(group__in=allgroups).distinct()
    serializer = MenuSerializer
    menu_list = get_permissions(serializer,permissions, 0)
    return JsonResponse({"data": menu_list})


def all_permissions(request):
    permissions = Permission.objects.all()
    serializer = MenuSerializer
    menu_list=get_permissions(serializer,permissions,1)
    return JsonResponse({"data": menu_list})
