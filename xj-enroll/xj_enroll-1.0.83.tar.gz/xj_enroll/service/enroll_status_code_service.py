# encoding: utf-8
"""
@project: djangoModel->enroll_status_code_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名状态码服务
@created_time: 2022/11/13 16:41
"""
from django.db import transaction
from django.db.models import F

from ..models import Enroll, EnrollRecord, EnrollSubitem, EnrollSubitemRecord


class EnrollStatusCodeService():
    @staticmethod
    def batcch_edit_code(enroll_id, code, edit_types=None):
        if edit_types is None:
            edit_types = ["enroll", "enroll_record", "enroll_subitem", "enroll_subitem_record"]
        sid = transaction.savepoint()
        try:
            if "enroll" in edit_types:
                enroll_query_obj = Enroll.objects.filter(id=enroll_id)
                enroll_query_obj.update(enroll_status_code=code)

            if "enroll_record" in edit_types:
                enroll_record_query_obj = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124)
                enroll_record_query_obj.update(enroll_status_code=code)

            if "enroll_subitem" in edit_types:
                enroll_subitem_query_obj = EnrollSubitem.objects.filter(enroll_id=enroll_id).exclude(enroll_subitem_status_code=124)
                enroll_subitem_query_obj.update(enroll_subitem_status_code=code)

            if "enroll_subitem_record" in edit_types:
                enroll_subitem_record_query_obj = EnrollSubitemRecord.objects.annotate(enroll_id=F("enroll_record__enroll_id")).filter(enroll_id=enroll_id).exclude(enroll_subitem_status_code=124)
                enroll_subitem_record_query_obj.update(enroll_subitem_status_code=code)

            transaction.clean_savepoints()
            return None, None
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return None, str(e)
