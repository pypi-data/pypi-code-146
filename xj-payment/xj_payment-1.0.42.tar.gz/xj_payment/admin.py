from django.contrib import admin

# 引入用户平台
from .models import *

class PaymentStatusAdmin(admin.ModelAdmin):

    fields = ('id', 'payment_status', 'group', 'description')
    list_display = ('id', 'payment_status', 'group', 'description')
    readonly_fields = ['id']

admin.site.register(PaymentStatus, PaymentStatusAdmin)


class PaymentPaymentAdmin(admin.ModelAdmin):

    fields = ('id', 'enroll_id', 'order_id', 'order_no', 'transact_no', 'transact_id', 'user_id', 'subject', 'total_amount', 'buyer_pay_amount', 'point_amount', 'invoice_amount', 'price_off_amount', 'pay_mode',)
    list_display = ('id','enroll_id', 'order_id', 'order_no', 'transact_no', 'transact_id', 'user_id', 'subject', 'total_amount', 'buyer_pay_amount', 'point_amount', 'invoice_amount', 'price_off_amount', 'pay_mode',)
    readonly_fields = ['id']

admin.site.register(PaymentPayment, PaymentPaymentAdmin)
