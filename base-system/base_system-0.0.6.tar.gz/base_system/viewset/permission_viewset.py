import datetime

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from base_system.models import ContentTypeCates, ContentTypeEx
from base_system.serializers_folder.permission_serializers import PermissionSerializer, MenuSerializer


class MenuViewSet(ModelViewSet):
    queryset = ContentTypeCates.objects.filter(is_active=True, parent=None)
    serializer_class = MenuSerializer
    pagination_class = None
    filter_fields = "__all__"


def get_permissions(serializer,permissions,value):
    content_type_ids = list(map(lambda perm: perm.content_type_id, permissions))
    content_type_ex = ContentTypeEx.objects.filter(is_active=True,content_type_id__in=content_type_ids)
    content_type_cat_ids = list(map(lambda cat: cat.content_type_cat_id, content_type_ex))
    content_type_cats = ContentTypeCates.objects.filter(id__in=content_type_cat_ids).order_by('order_by')
    rel_list = []
    for rel in content_type_cats:
        get_parent(rel_list, rel)
    rel_list += content_type_cats
    rel_list = list(set(rel_list))
    serializer_rels = serializer(rel_list, many=True)
    all_menu = serializer_rels.data

    menu_list = [menu for menu in all_menu if not menu['parent']]
    for menu_1 in all_menu:
        children_list = [children for children in all_menu if children['parent'] == int(menu_1['id'].replace('n',''))]
        children_list = sorted(children_list, key=lambda x: x['order_by'])
        menu_1['children'] = children_list
        content_type_ex = ContentTypeEx.objects.filter(content_type_cat_id=int(menu_1['id'].replace('n',''))).first()
        if value:
            if content_type_ex and children_list ==[]:
                menu_1["children"] = list(map(lambda p: {"id": p.id, "name": p.name, "codename": p.codename},
                                                 content_type_ex.content_type.permission_set.all()))
    menu_list = sorted(menu_list, key=lambda x: x['order_by'])
    return menu_list


def menu_permissions(request):
    permissions = Permission.objects.all()
    serializer = MenuSerializer
    menu_list = get_permissions(serializer, permissions, 1)
    return JsonResponse({"data": menu_list})


def get_parent(li, rels):
    if rels.parent:
        if rels.parent not in li:
            li.append(rels.parent)
            get_parent(li, rels.parent)
    return li
