import random

from django.http import HttpResponse
from django.utils import timezone


# from ..services.payment_service import PaymentService
from xj_enroll.service.enroll_services import EnrollServices
from ..utils.alipay_utils import *
from ..utils.common import get_domain

from config.config import JConfig
config = JConfig()
gatway = config.get("xj_payment", "GATEWAY", "https://openapi.alipaydev.com/gateway.do")


class PaymentAlipayService:
    @staticmethod
    def get_pay_url(params, host):
        # 生成支付宝支付链接地址
        domain_name = get_domain(host)
        money = params['money']
        out_trade_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(map(str, random.sample(range(0, 9), 6)))
        notify_url = domain_name + '/api/payment/update_order/'
        alipay = my_ali_pay(notify_url)
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=params['out_trade_no'],  # 订单编号
            total_amount=str(money),  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
            subject=f"紫薇系统-{params['out_trade_no']}",  # 商品名称或产品名称
            return_url=domain_name + "/api/payment/get_result/",  # 支付成功后跳转的页面，App支付此参数无效，集成支付宝SDK自带跳转
        )
        # 拼接支付链接，注意：App支付不需要返回支付宝网关
        ali_pay_url = order_string if is_app_pay(order_string) else gatway + "?" + order_string
        ali_pay_url = {
            'ali_pay_url': ali_pay_url,
        }
        return ali_pay_url, None

    @staticmethod
    def pay_result(data):
        ali_pay = my_ali_pay()
        sign = data.pop('sign', None)
        success = ali_pay.verify(data, sign)
        if success:
            return None, None
        return None, '支付失败'

    @staticmethod
    def update_order(data):
        payment = None
        refund = None
        close = None
        try:
            gmt_payment = data.get('gmt_payment', [None])
            payment = gmt_payment[0]
            gmt_refund = data.get('gmt_refund', [None])
            refund = gmt_refund[0]
            gmt_close = data.get('gmt_close', [None])
            close = gmt_close[0]
        except KeyError as e:
            print(data)

        callback_data = {
            'app_id': data['app_id'][0],
            'order_no': data['out_trade_no'][0],
            'transact_no': data['trade_no'][0],
            'subject': data['subject'][0],
            'total_amount': data['total_amount'][0],
            'buyer_pay_amount': data['buyer_pay_amount'][0],
            'point_amount': data['point_amount'][0],
            'invoice_amount': data['invoice_amount'][0],
            'pay_mode': 1,
            'order_time': data['gmt_create'][0],
            'payment_time': payment,
            'refunt_time': refund,
            'close_time': close,
            # 'voucher_detail': data['vocher_detail_list']
        }
        if data['trade_status'][0] == 'WAIT_BUYER_PAY':
            callback_data['payment_status_id'] = 1  # 交易创建
        elif data['trade_status'][0] == 'TRADE_CLOSED':
            callback_data['payment_status_id'] = 2  # 交易关闭
        elif data['trade_status'][0] == 'TRADE_SUCCESS':
            callback_data['payment_status_id'] = 3  # 交易成功
        elif data['trade_status'][0] == 'TRADE_FINISHED':
            callback_data['payment_status_id'] = 4  # 交易完结
        else:
            callback_data['payment_status_id'] = ''

        data = {k: v[0] for k, v in data.items()}

        ali_pay = my_ali_pay()
        sign = data.pop('sign', None)
        success = ali_pay.verify(data, sign)  # 返回验签结果, True/False
        print("异步通知验证状态: ", success)
        if success:
            # 此处写支付验签成功修改订单状态相关业务逻辑
            # PaymentService.create(callback_data)
            data, err = EnrollServices.pay_call_back(callback_data["order_no"])
            print("pay_call_back:", data, err)
            return HttpResponse('success')  # 返回success给支付宝服务器, 若支付宝收不到success字符会重复发送通知
        return HttpResponse('fail')

        # 实例化支付类
        alipay = my_ali_pay()
        # 调用退款方法
        domain_name = get_domain(self)
        notify_url = domain_name + '/api/payment/update_order/'
        order_string = alipay.api_alipay_trade_refund(
            # 订单号，一定要注意，这是支付成功后返回的唯一订单号
            out_trade_no=str(out_trade_no),
            # 退款金额，注意精确到分，不要超过订单支付总金额
            refund_amount=money,
            # 回调网址
            notify_url=notify_url
        )

    @staticmethod
    def refund(params, host):
        alipay = my_ali_pay()
        # 调用退款方法
        domain_name = get_domain(host)
        notify_url = domain_name + '/api/payment/update_order/'
        order_string = alipay.api_alipay_trade_refund(
            # 订单号，一定要注意，这是支付成功后返回的唯一订单号
            out_trade_no=str(params['out_trade_no']),
            # 退款金额，注意精确到分，不要超过订单支付总金额
            refund_amount=params['money'],
            # 回调网址
            notify_url=notify_url
        )
        return order_string, None
