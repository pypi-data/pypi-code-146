# 应用名称
from django.urls import re_path

from xj_payment.apis import alipay, transaction_inquiry, wechat, payment, payment_status
from .apis import payment_alipay
from .apis import payment_wechat
from .apis import payment_unionpay
from .apis import payment
from .apis import wechat

app_name = 'payment'

urlpatterns = [
    # re_path(r'^alipay_payment/?$', alipay.Payment.as_view(), ),
    # re_path(r'^alipay_payment/?$', alipay.Payment.test)
    # re_path(r'^get_pay_url/?$', alipay.Payment.get_pay_url),  # 获取支付宝支付链接
    re_path(r'^get_pay_url/?$', payment_alipay.PaymentAlipay.get_pay_url),  # 获取支付宝支付链接
    # re_path(r'^get_result/?$', alipay.Payment.pay_result),  # 支付宝处理完成后同步回调通知
    re_path(r'^get_result/?$', payment_alipay.PaymentAlipay.pay_result),  # 支付宝处理完成后同步回调通知
    re_path(r'^update_order/?$', alipay.Payment.update_order),  # 支付宝处理完成后支付宝服务器异步回调通知
    # re_path(r'^refund/?$', alipay.Payment.refund),  # 支付宝退款
    re_path(r'^close/?$', alipay.Payment.close),  # 关闭订单

    re_path(r'^refund_inquiry/?$', transaction_inquiry.query.refund_inquiry),  # 支付宝退款查询
    re_path(r'^trade_query/?$', transaction_inquiry.query.trade_query),  # 支付宝下单查询

    re_path(r'^get_user_info/?$', payment_wechat.PaymentWechat.get_user_info),  # 获取用户标识接口
    re_path(r'^applets_pay/?$', payment_wechat.PaymentWechat.payment_applets_pay),  # 小程序支付接口
    re_path(r'^wechat_py/?$', wechat.WeChatPayment.pay),  # 微信支付接口
    re_path(r'^scan_pay/?$', payment_wechat.PaymentWechat.payment_scan_pay),  # 微信扫码支付
    re_path(r'^red_envelopes/?$', payment_wechat.PaymentWechat.payment_red_envelopes),  # 微信红包
    re_path(r'^wechat_callback/?$', payment_wechat.PaymentWechat.callback),  # 微信回调接口
    re_path(r'^wechat_callback_v3/?$', payment_wechat.PaymentWechat.callback_v3),  # 微信回调接口v3

    re_path(r'^unipay/?$', payment_unionpay.PaymentUnionPay.unipay),

    re_path(r'^pay/?$', payment.Payment.pay),  # 支付总接接口

    re_path(r'^refund/?$', payment.Payment.refund),

    re_path(r'^list/?$', payment.Payment.get),  # 支付列表

    re_path(r'^status/?$', payment_status.PaymentStatus.as_view()),  # 支付状态列表

    # re_path(r'^pay/?$', wechat_payment.WeChatPayment.pay),
    # re_path(r'^pay/?$', wechat.WeChatPayment.pay),
    # 支付结果回调
    # re_path(r'^payNotify/', views.WeChatPayNotifyViewSet.as_view(), name='pay_notify'),

]
