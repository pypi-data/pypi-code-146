from django.db import models


# Create your models here.

# 1、Payment_Status  支付状态表 [NF1]
class PaymentStatus(models.Model):
    payment_status = models.CharField(verbose_name='支付状态', max_length=128, blank=True, null=True, db_index=True)
    group = models.CharField(verbose_name='分组', max_length=128, blank=True, null=True, db_index=True)
    description = models.CharField(verbose_name='描述', max_length=128, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'payment_status'
        verbose_name_plural = "01. 支付状态表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.payment_status}"


# 2、payment_payment  支付订单记录表 [NF1]
class PaymentPayment(models.Model):
    # id = models.AutoField(verbose_name='id', blank=True, null=False, db_index=True)
    order_no = models.BigIntegerField(verbose_name='订单号', blank=True, null=False, db_index=True)
    # transact_no = models.IntegerField(verbose_name='流水号', blank=True, null=False, db_index=True)
    transact_no = models.CharField(verbose_name='交易号', max_length=128, blank=True, null=True, db_index=True)
    # transact_id = models.IntegerField(verbose_name='资金id', blank=True, null=True, db_index=True)
    transact_id = models.CharField(verbose_name='资金交易ID', max_length=128, blank=True, null=True, db_index=True)
    enroll_id = models.IntegerField(verbose_name='报名id', blank=True, null=False, db_index=True)
    order_id = models.IntegerField(verbose_name='订单id', blank=True, null=False, db_index=True)
    user_id = models.IntegerField(verbose_name='用户id', blank=True, null=True, db_index=True)
    subject = models.CharField(verbose_name='商品标题', max_length=128, blank=True, null=True, db_index=True)
    total_amount = models.DecimalField(verbose_name='订单金额', max_digits=11, decimal_places=2, blank=True, null=True)
    buyer_pay_amount = models.DecimalField(verbose_name='用户支付金额', max_digits=11, decimal_places=2, blank=True,
                                           null=True)
    point_amount = models.DecimalField(verbose_name='积分点(集分宝)抵扣金额', max_digits=11, decimal_places=2, blank=True,
                                       null=True)
    invoice_amount = models.DecimalField(verbose_name='开票金额', max_digits=11, decimal_places=2, blank=True, null=True)
    price_off_amount = models.DecimalField(verbose_name='折扣金额', max_digits=11, decimal_places=2, blank=True, null=True)
    payment_type = (
        ("UNKNOWN", 'UNKNOWN'),
        ("ALIPAY", 'ALIPAY'),
        ("WECHAT", 'WECHAT'),
        ("UNION_PA", 'UNION_PA'),
    )
    pay_mode = models.CharField(verbose_name='支付类型', max_length=128, choices=payment_type)
    order_status_id = models.IntegerField(verbose_name='订单状态（十数法）', blank=True, null=True, db_index=True)
    payment_status = models.ForeignKey(PaymentStatus, verbose_name='支付状态', blank=True, null=True,
                                       on_delete=models.DO_NOTHING)
    nonce_str = models.JSONField(verbose_name='临时字段', max_length=128, blank=True, null=True, db_index=True)
    order_time = models.DateTimeField(verbose_name='订单创建时间', blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, )
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True, blank=True, null=True, )
    payment_time = models.DateTimeField(verbose_name='支付时间', blank=True, null=True)
    refunt_time = models.DateTimeField(verbose_name='退款时间', blank=True, null=True)
    close_time = models.DateTimeField(verbose_name='退款时间', blank=True, null=True)
    voucher_detail = models.JSONField(verbose_name='优惠券详细信息', max_length=128, blank=True, null=True, db_index=True)
    snapshot = models.CharField(verbose_name='商品快照', max_length=128, blank=True, null=True, db_index=True)
    more = models.CharField(verbose_name='辅助信息', max_length=128, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'payment_payment'
        verbose_name_plural = "02. 支付订单记录表"

    def __str__(self):
        # return self.subject if self.subject else ""
        return f"{self.order_no}"
