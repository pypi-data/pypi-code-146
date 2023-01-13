from django.contrib import admin

# 引入用户平台
from .models import PayMode, Currency, Transact, SandBox


# Register your models here.


class PayModeAdmin(admin.ModelAdmin):
    fields = ('id', 'pay_mode', "pay_value")
    list_display = ('id', 'pay_mode', "pay_value")
    search_fields = ('id', 'pay_mode' "pay_value",)
    readonly_fields = ['id']


class CurrencyAdmin(admin.ModelAdmin):
    fields = ('id', 'currency',)
    list_display = ('id', 'currency',)
    search_fields = ('id', 'currency',)
    readonly_fields = ['id']


class SandBoxAdmin(admin.ModelAdmin):
    fields = ('id', 'sand_box_name',)
    list_display = ('id', 'sand_box_name',)
    search_fields = ('id', 'sand_box_name',)
    readonly_fields = ['id']


class TransactAdmin(admin.ModelAdmin):
    fields = ('id', 'account', 'their_account', 'transact_no', 'enroll_id', 'transact_time', 'platform_id', 'order_no',
              'opposite_account', 'summary', 'currency', 'income', 'outgo', 'balance', 'pay_mode', 'goods_info',
              'pay_info', 'remark', 'images', 'sand_box', 'is_reverse',)
    list_display = (
        'id', 'account', 'their_account', 'transact_no', 'enroll_id', 'transact_time', 'platform_id', 'order_no',
        'opposite_account', 'summary', 'currency', 'income', 'outgo', 'balance', 'pay_mode', 'goods_info',
        'pay_info', 'remark', 'images', 'sand_box', 'is_reverse',)
    search_fields = (
        'id', 'account', 'their_account', 'transact_no', 'enroll_id', 'transact_time', 'platform_id', 'order_no',
        'opposite_account', 'summary', 'currency', 'income', 'outgo', 'balance', 'pay_mode', 'goods_info',
        'pay_info', 'remark', 'images', 'sand_box', 'is_reverse',)
    # list_filter = ['platform', 'currency', 'account', 'their_account', 'order_no']
    readonly_fields = ['id', 'transact_time']
    # def platform(self, obj):
    #     return obj.platform

    # 不起作用 https://docs.djangoproject.com/zh-hans/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    # @admin.display(description='Name')
    # def transact_time(self, obj):
    #     return "2424"


admin.site.register(Transact, TransactAdmin)
admin.site.register(PayMode, PayModeAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(SandBox, SandBoxAdmin)
