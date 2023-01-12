from django.contrib import admin

from .models import *


class EnrollAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'thread_id', 'trading_relate', 'region_code', 'occupy_room', 'enroll_status_code', 'min_number',
        'max_number', 'min_count_apiece', 'max_count_apiece', 'enroll_rule_group', 'price', 'count', 'unit', 'fee',
        'reduction', 'subitems_amount', 'amount', 'paid_amount', 'unpaid_amount', 'commision', 'deposit', 'hide_price',
        'hide_user', 'has_repeat', 'has_subitem', 'has_audit', 'need_vouch', 'need_deposit',
        'need_imprest', 'enable_pool', 'pool_limit', 'pool_stopwatch', 'open_time', 'close_time', 'launch_time',
        'finish_time', 'spend_time', 'create_time', 'update_time', 'snapshot', 'remark',
    )
    search_fields = ('id', 'thread_id', 'trading_relate', 'region_code', 'occupy_room', 'enroll_status_code', 'min_number',)
    fields = (
        'id', 'thread_id', 'trading_relate', 'region_code', 'occupy_room', 'enroll_status_code', 'min_number', 'max_number', 'min_count_apiece', 'max_count_apiece', 'enroll_rule_group', 'price',
        'count', 'unit', 'fee', 'has_repeat', 'has_subitem', 'has_audit', 'need_vouch', 'need_deposit', 'need_imprest', 'enable_pool', 'pool_limit', 'pool_stopwatch', 'open_time', 'close_time',
        'launch_time', 'finish_time', 'spend_time', 'create_time', 'update_time', 'snapshot', 'remark',
    )
    readonly_fields = ['id', 'update_time']


class EnrollSubitemAdmin(admin.ModelAdmin):
    list_display = ('id', 'enroll_id', 'name', 'price', 'count', 'unit', 'amount', 'description', 'remark', 'enroll_subitem_status_code',
                    'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
                    'field_10',)
    search_fields = ('id', 'enroll_id', 'name', 'price', 'count', 'unit', 'amount', 'description', 'remark',
                     'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
                     'field_10',)
    fields = ('id', 'enroll_id', 'name', 'price', 'count', 'unit', 'amount', 'description', 'remark', 'enroll_subitem_status_code',
              'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
              'field_10',)
    readonly_fields = ['id']


class EnrollAuthStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    search_fields = ('id', 'value')
    fields = ('id', 'value',)
    readonly_fields = ['id']


class EnrollPayStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    search_fields = ('id', 'value')
    fields = ('id', 'value',)
    readonly_fields = ['id']


class EnrollRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'enroll', 'user_id', 'enroll_auth_status_id', 'enroll_pay_status_id', 'enroll_status_code',
                    'create_time', 'price', 'deposit', 'count', 'main_amount', 'coupon_amount', 'again_reduction',
                    'subitems_amount', 'deposit_amount', 'amount', 'paid_amount', 'unpaid_amount',
                    'fee', 'photos', 'files', 'score', 'reply', 'remark',)
    search_fields = ('id', 'enroll', 'user_id', 'enroll_auth_status_id', 'enroll_pay_status_id', 'enroll_status_code',
                     'create_time', 'price', 'deposit', 'count', 'main_amount', 'coupon_amount', 'again_reduction',
                     'subitems_amount', 'deposit_amount', 'amount', 'paid_amount', 'unpaid_amount',
                     'fee', 'photos', 'files', 'score', 'reply', 'remark',)
    fields = ('id', 'enroll', 'user_id', 'enroll_auth_status_id', 'enroll_pay_status_id', 'enroll_status_code',
              'create_time', 'price', 'deposit', 'count', 'main_amount', 'coupon_amount', 'again_reduction',
              'subitems_amount', 'deposit_amount', 'amount', 'paid_amount', 'unpaid_amount',
              'fee', 'photos', 'files', 'score', 'reply', 'remark',)
    readonly_fields = ['id']


class EnrollRecordSubitemAdmin(admin.ModelAdmin):
    list_display = ('id', 'enroll_record', 'enroll_subitem', 'user_id', 'price', 'count', 'subitem_amount', 'enroll_subitem_status_code', "reply", "remark", "files", "photos",)
    search_fields = ('id', 'enroll_record', 'enroll_subitem', 'user_id', 'price', 'count', 'subitem_amount',)
    fields = ('id', 'enroll_record', 'enroll_subitem', 'user_id', 'price', 'count', 'subitem_amount', 'enroll_subitem_status_code', "reply", "remark", "files", "photos",)
    readonly_fields = ['id', ]


class EnrollRuleGroupAdmin(admin.ModelAdmin):
    list_display = ('id', "classify_id", 'rule_group', 'category_id', 'description',)
    search_fields = ('id', "classify_id", 'rule_group', 'category_id', 'description',)
    fields = ('id', 'rule_group', "classify_id", 'category_id', 'description',)
    readonly_fields = ['id', ]


class EnrollRuleValuateAdmin(admin.ModelAdmin):
    list_display = ('id', 'enroll_rule_group', 'name', 'type', 'field', 'expression_string', 'sort')
    search_fields = ('id', 'enroll_rule_group', 'name', 'type', 'field', 'expression_string',)
    fields = ('id', 'enroll_rule_group', 'name', 'type', 'field', 'expression_string', 'sort')
    readonly_fields = ['id', ]
    ordering = ("-enroll_rule_group", '-sort',)


class EnrollStatusCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'enroll_status_code', 'value', "config")
    search_fields = ('id', 'enroll_status_code', 'value')
    fields = ('id', 'enroll_status_code', 'value', "config")
    readonly_fields = ['id', ]


admin.site.register(EnrollStatusCode, EnrollStatusCodeAdmin)
admin.site.register(Enroll, EnrollAdmin)
admin.site.register(EnrollAuthStatus, EnrollAuthStatusAdmin)
admin.site.register(EnrollPayStatus, EnrollPayStatusAdmin)
admin.site.register(EnrollRecord, EnrollRecordAdmin)
admin.site.register(EnrollSubitem, EnrollSubitemAdmin)
admin.site.register(EnrollSubitemRecord, EnrollRecordSubitemAdmin)
admin.site.register(EnrollRuleGroup, EnrollRuleGroupAdmin)
admin.site.register(EnrollRuleValuate, EnrollRuleValuateAdmin)
