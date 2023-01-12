from django.urls import re_path

from .api.enroll_apis import EnrollAPI
from .api.enroll_statistics_apis import EnrollStatisticsAPI
from .api.enroll_status_code_api import EnrollStatusCodeAPI
from .api.rarely_data_list_api import OtherListAPIView
from .api.record_apis import RecordAPI
from .api.rule_apis import RuleAPI
from .api.subitem_apis import SubitemApis
from .api.subitem_record_apis import SubitemRecordApis
from .api.valuation_api import ValuationAPIView
from .service_register import register

# 对服务进行，注册可直接访问，提过流程模块等调度模块调用
register()

urlpatterns = [
    # 报名API
    re_path(r'^list/?$', EnrollAPI.list),
    re_path(r'^own_list/?$', EnrollAPI.own_list),
    re_path(r'^undertake_list/?$', EnrollAPI.undertake_list),
    re_path(r'^detail/?(?P<enroll_id>\d+)?$', EnrollAPI.detail),
    re_path(r'^edit/?(?P<enroll_id>\d+)?$', EnrollAPI.edit),
    re_path(r'^delete/?(?P<enroll_id>\d+)?$', EnrollAPI.delete),
    re_path(r'^add/?$', EnrollAPI.add),
    re_path(r'^enroll/?$', EnrollAPI.enroll),  # 报名记录联合添加报名记录和分项记录, 当前逻辑暂不使用
    re_path(r'^pay_callback/?$', EnrollAPI.enroll_pay_callback),

    # 报名记录
    re_path(r'^record_list/?$', RecordAPI.list),
    re_path(r'^record_add/?$', RecordAPI.add),
    # re_path(r'^record_del/?(?P<pk>\d+)?$', RecordAPI.record_del), // 记录没有删除这个流程节点
    re_path(r'^record_edit/?(?P<pk>\d+)?$', RecordAPI.record_edit),
    re_path(r'^record_detail/?(?P<pk>\d+)?$', RecordAPI.record_detail),
    re_path(r'^appoint/?$', RecordAPI.appoint),

    # 报名分项
    re_path(r'^subitem_add/?$', SubitemApis.add),
    re_path(r'^subitem_detail/?(?P<pk>\d+)?$', SubitemApis.detail),
    re_path(r'^subitem_batch_add/?$', SubitemApis.batch_add),
    re_path(r'^subitem_list/?$', SubitemApis.list),
    re_path(r'^subitem_edit/?(?P<pk>\d+)?$', SubitemApis.edit),
    re_path(r'^subitem_batch_edit/?$', SubitemApis.batch_edit),
    re_path(r'^subitem_edit_by_enroll/?(?P<enroll_id>\d+)?$', SubitemApis.edit_by_enroll_id),  #
    re_path(r'^subitem_extend_field/?$', SubitemApis.extend_field),

    # 报名分项记录
    re_path(r'^subitem_record_add/?$', SubitemRecordApis.add),

    # re_path(r'^subitem_record_del/?(?P<pk>\d+)?$', SubitemRecordApis.delete), // 记录没有删除这个流程节点
    re_path(r'^subitem_record_list/?$', SubitemRecordApis.list),
    re_path(r'^subitem_record_edit/?(?P<pk>\d+)?$', SubitemRecordApis.edit),
    re_path(r'^subitem_record_batch_add/?$', SubitemRecordApis.batch_add),

    # 报名规则
    re_path(r'^rule_list/?$', RuleAPI.list),
    re_path(r'^rule_edit/?(?P<rule_value_id>\d+)?$', RuleAPI.edit),
    re_path(r'^rule_delete/?(?P<rule_value_id>\d+)?$', RuleAPI.delete),
    re_path(r'^rule_add/?$', RuleAPI.add),
    re_path(r'^rule_group_list/?$', RuleAPI.group_list),  # 分组列表

    # 计价接口
    re_path(r'^valuation/?$', ValuationAPIView.valuate),
    re_path(r'^valuation_test/?$', ValuationAPIView.valuate_test),
    re_path(r'^valuation_detailed_list/?(?P<enroll_id>\d+)?$', ValuationAPIView.valuation_detailed_list),

    # 非热更新列表返回
    re_path(r'^status_code/?$', OtherListAPIView.enroll_status_code),

    # 报名统计
    re_path(r'^statistics/?$', EnrollStatisticsAPI.statistics),
    re_path(r'^statistics_by_user/?$', EnrollStatisticsAPI.statistics_by_user),

    # 报名状态接口
    re_path(r'^batch_edit_code/?$', EnrollStatusCodeAPI.batch_edit_code),
]
