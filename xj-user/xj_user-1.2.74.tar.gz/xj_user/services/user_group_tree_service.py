import json

from django.core import serializers


from ..models import Group, BaseInfo

tree = []
index = 0


class UserGroupTreeService():
    @staticmethod
    def tree_loop(parent_group=0, level=1):
        first_level = Group.objects.filter(parent_group=parent_group).to_json()
        if not first_level:
            return []
        for j in first_level:
            j['children'] = UserGroupTreeService.tree_loop(j['id'])
        return first_level

    def parse_model(res_set, need_all=False):
        json_data = json.loads(serializers.serialize('json', res_set))
        if not json_data:
            return None
        else:
            if not need_all:
                return json_data[0]['fields']
            else:
                return [i['fields'] for i in json_data]

    @staticmethod
    def getTree(list, parent_group):
        tree = []
        for item in list:
            if item['parent_group'] == str(parent_group):
                item['children'] = UserGroupTreeService.getTree(list, item['id'])
                tree.append(item)

        return tree

    @staticmethod
    def getTrees(list, parent_group):
        tree = []
        if parent_group != 0:
            a = UserGroupTreeService.grop(parent_group)
            print(a)
            for item in list:
                if item['parent_group'] == str(parent_group):
                    item['children'] = UserGroupTreeService.getTree(list, item['id'])
                    tree.append(item)
            a[0]['children'] = tree
            return a[0]
        else:
            for item in list:
                if item['parent_group'] == str(parent_group):
                    item['children'] = UserGroupTreeService.getTree(list, item['id'])
                    tree.append(item)

        return tree

    @staticmethod
    def grop(id):
        gruop = Group.objects.filter(id=id).to_json()
        return gruop

    @staticmethod
    def group_tree(user_id):
        user_group_id = BaseInfo.objects.filter(id=user_id).first().to_json()
        # print(user_group_id['user_group_id'])
        first_level = Group.objects.filter().to_json()
        group_tree = UserGroupTreeService.getTrees(first_level, user_group_id['user_group_id'])
        return group_tree, None
