# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""

from ..models import Thread
from ..models import ThreadExtendData
from ..serializers import ThreadDetailSerializer
from ..services.thread_extend_service import ThreadExtendService
from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import format_params_handle


# 信息服务CURD(支持扩展字段配置)  V2版本
class ThreadItemService:
    @staticmethod
    def add(params):
        # 扩展字段与主表字段拆分
        filter_filed_list = [  # 主表过滤字段
            "category_id", 'classify_id', 'show_id', 'user_id', 'auth_id', 'title', 'content', 'summary', 'ip',
            'has_enroll', 'has_fee', "sort"
            'has_comment', 'cover', "video", "photos", 'files', "price", "author", "create_time", "logs", "more"
        ]
        # 主表插入
        main_form_data = format_params_handle(
            params.copy(), filter_filed_list=filter_filed_list,
            alias_dict={'category_id': 'category_id_id', 'classify_id': 'classify_id_id'}
        )
        try:
            instance = Thread.objects.create(**main_form_data)
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(e.__traceback__.tb_lineno)}'''
        # 扩展表插入或更新
        except_main_form_data = format_params_handle(params.copy(), remove_filed_list=filter_filed_list)
        ThreadExtendService.create_or_update(except_main_form_data, instance.id, main_form_data.get("category_id_id", None))
        return {"id": instance.id}, None

    @staticmethod
    def detail(pk):
        """获取信息内容"""
        try:
            thread_obj = Thread.objects.filter(id=pk, is_deleted=False).first()
            # print("ThreadItemService detail thread_obj:", thread_obj)
            if not thread_obj:  # 信息统计表更新数据
                return None, "数据不存在"
            StatisticsService.increment(thread_id=thread_obj.id, tag='views', step=1)
            res_set = dict(ThreadDetailSerializer(thread_obj).data)
            res_set.update(res_set.pop('statistic'))
            res_set.update(res_set.pop('thread_extends'))
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(e.__traceback__.tb_lineno)}'''
            # 扁平化数据
        return res_set, 0

    @staticmethod
    def edit(form_data, pk):
        form_data.setdefault("id", pk)
        # 主表过滤字段
        filter_filed_list = [
            "category_id", 'classify_id', 'show_id', 'user_id', 'auth_id', 'title', 'content', 'summary', 'ip', 'has_enroll', 'has_fee',
            'has_comment', 'cover', "video", "photos", 'files', "price", "author", "create_time", "logs", "more", "sort"
        ]
        # 主表修改
        main_res = Thread.objects.filter(id=pk)
        if not main_res:
            return None, "数据不存在，无法进行修改"
        try:
            # 主表修改
            main_form_data = format_params_handle(form_data.copy(), filter_filed_list=filter_filed_list)
            main_res.update(**main_form_data)
            # 扩展字段修改
            except_main_form_data = format_params_handle(form_data.copy(), remove_filed_list=filter_filed_list)  # 排除主表之外的字段，理论上就是扩展字段，接下来仅仅需要转换一下扩展字段
            return ThreadExtendService.create_or_update(except_main_form_data, pk, main_form_data.get("category_id", None))
        except Exception as e:
            return None, "信息主表写入异常：" + str(e) + "  line:" + str(e.__traceback__.tb_lineno)

    @staticmethod
    def delete(id):
        main_res = Thread.objects.filter(id=id, is_deleted=0)
        if not main_res:
            return None, "数据不存在，无法进行修改"
        main_res.update(is_deleted=1)
        return None, None

    @staticmethod
    def select_extend(id):
        """单独查询 查询扩展字段"""
        return util_response(list(ThreadExtendData.objects.filter(id=id).values()))
