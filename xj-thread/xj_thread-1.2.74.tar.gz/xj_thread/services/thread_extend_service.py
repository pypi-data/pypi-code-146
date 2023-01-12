# encoding: utf-8
"""
@project: djangoModel->extend_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 扩展服务
@created_time: 2022/7/29 15:14
"""
from django.db.models import F

from ..models import ThreadExtendField, Thread, ThreadExtendData


# 服务提供 扩展表的字段映射关系，返回映射后KEY名。
# 达意最好是ThreadExtendInsertService:
class ThreadExtendInputService:
    thread_extend_filed = None

    def __init__(self, form_data):
        """
        :param form_data: 表单
        :param need_all_field: 是否需要全部的扩展字段（查询的时候会用到）
        """
        self.form_data = form_data
        self.form_data['category_id_id'] = self.form_data.pop("category_id", None)
        self.form_data['classify_id_id'] = self.form_data.pop("classify_id", None)
        # 新增或者修改的时候
        self.thread_extend_filed = {}
        category_id = None
        if "id" in self.form_data.keys():  # 修改时候：传了id,没有传classify_id
            category_id = Thread.objects.filter(id=self.form_data.get('id')).first().category_id

        if self.form_data.get('category_id_id', None):
            category_id = self.form_data.get('category_id_id')

        if category_id:
            self.thread_extend_filed = {
                item["field"]: item["field_index"] for item in ThreadExtendField.objects.filter(category_id_id=category_id).values('field', 'field_index')
            }

    # 请求参数转换
    # TODO 弃用 sieyoo
    def transform_param(self):
        # 没有定义扩展映射直接返回，不进行扩展操作
        if self.thread_extend_filed is None:
            return self.form_data, None
        extend_data = {self.thread_extend_filed[k]: self.form_data.pop(k) for k, v in self.form_data.copy().items() if k in self.thread_extend_filed.keys()}
        return self.form_data, extend_data


# 所有的输出信息服务都需要有统一的公共方法
# 暂时定位 output
class ThreadExtendOutPutService():
    # extend_field:扩展数据表的字段如field_1,field_2....
    # field:配置的字段映射
    field_list = None
    extend_field_map = None  # {extend_field:field}
    field_map = None  # {field:extend_field}
    finish_data = None  # 最终完成映射的扩展数据字典

    def __init__(self, category_id_list=None, thread_id_list=None):
        if category_id_list is None:
            raise Exception("category_id_list 必传")
        if thread_id_list is None:
            raise Exception("thread_id_list 必传")
        self.category_id_list = category_id_list
        self.thread_id_list = thread_id_list

        # 字段映射关系
        field_list_set = ThreadExtendField.objects.filter(category_id__in=self.category_id_list)
        self.field_list = []
        if field_list_set:
            self.field_list = list(field_list_set.values())
        self.field_map = {}  # {i["category_id"]: {i["field_index"]: i["field"],....},....}
        for item in self.field_list:
            if self.field_map.get(item["category_id"]):
                self.field_map[item["category_id"]].update({item["field_index"]: item["field"]})
            else:
                self.field_map[item["category_id"]] = {item["field_index"]: item["field"]}

    def out_put(self):
        self.finish_data = {}  # 返回 self.finish_data：{thread_id:{扩展数据},.....} {thread_id:{扩展数据},.....}
        # 获取扩展数据
        extend_data = list(ThreadExtendData.objects.filter(thread_id__in=self.thread_id_list).annotate(category_id=F("thread_id__category_id")).values())
        extend_data = [(i.pop("thread_id_id"), i.pop("category_id"), i) for i in extend_data]
        # 扩展数据 替换KEY
        for thread_id, category_id, item in extend_data:
            category_field = self.field_map.get(category_id, None)
            if category_field is None:
                continue
            remove_none = {k: v for k, v in item.items() if v}
            temp_dict = {}
            for k, v in remove_none.items():
                if category_field.get(k):
                    temp_dict.update({category_field[k]: v})
            self.finish_data[thread_id] = temp_dict
        return self.finish_data

    def merge(self, merge_set, merge_set_key='id'):
        # 把结果集和{thread_id:{扩展数据}}，拼接到 merge_set
        extend_map = self.out_put()
        for item in merge_set:
            if item.get(merge_set_key) and extend_map.get(item[merge_set_key]):
                item.update(extend_map[item[merge_set_key]])
        return merge_set


# 扩展字段增删改查
class ThreadExtendService:
    @staticmethod
    def create_or_update(extend_params, thread_id=None, category_id=None, **kwargs):
        # 不存在扩展字段的时候直接返回成功
        if extend_params is None:
            return None, None
        if thread_id is None:
            return None, "扩展字段修改错误,thread_id不可以为空"
        # 获取扩展字段映射
        thread_obj = Thread.objects.filter(id=thread_id).first()
        if not thread_obj and not category_id:
            return None, None
        category_id = category_id if category_id else thread_obj.category_id
        # 扩展字段映射
        extend_fields = ThreadExtendField.objects.filter(category_id=category_id).values("field_index", "field")
        extend_field_map = {item["field"]: item["field_index"] for item in extend_fields}
        # 扩展数据替换
        transformed_extend_params = {extend_field_map[k]: v for k, v in extend_params.items() if extend_field_map.get(k)}
        # 修改或添加数据
        try:
            extend_obj = ThreadExtendData.objects.filter(thread_id=thread_id)
            if not extend_obj:
                transformed_extend_params.setdefault('thread_id_id', thread_id)
                ThreadExtendData.objects.create(**transformed_extend_params)
                return None, None
            extend_obj.update(**transformed_extend_params)
        except Exception as e:
            return None, "扩展字段修改错误:" + str(e)
        return None, None
