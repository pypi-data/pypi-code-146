import random
from urllib import parse

from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from xj_payment.common import get_domain
# from xj_payment.services.payment_service import PaymentService
from xj_payment.utils.utils_v1 import my_ali_pay, is_app_pay


# redis连接对象

# redis = Redis().connection()


class Payment(APIView):

    def get_pay_url(self):
        """
        获取支付连接
        :param request:
        :return:
        """
        if self.method == "GET":
            order_id = self.GET.get('order_id', 0)  # 前端传回的订单id
            money = self.GET.get('price')  # 前端传回的金额数据
            out_trade_no = self.GET.get('out_trade_no')  # 前端传回的订单号

            # if not all([order_id, money]):
            #     return JsonResponse(dict(message="参数错误"))

            # 此处可增加根据订单id查询判断该订单是否存在相关业务逻辑
            # 组织订单编号：当前时间字符串 + 6位随机数 ---> 20200808154711123456
            out_trade_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(map(str, random.sample(range(0, 9), 6)))
            # 生成支付宝支付链接地址
            domain_name = get_domain(self)
            notify_url = domain_name + '/api/payment/update_order/'
            alipay = my_ali_pay(notify_url)
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=out_trade_no,  # 订单编号
                total_amount=str(money),  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
                subject=f"紫薇系统-{out_trade_no}",  # 商品名称或产品名称
                return_url=domain_name + "/api/payment/get_result/",  # 支付成功后跳转的页面，App支付此参数无效，集成支付宝SDK自带跳转
            )
            gatway = Config.getIns().get("xj_payment", "GATEWAY", "https://openapi.alipaydev.com/gateway.do")
            # print(123)
            # 拼接支付链接，注意：App支付不需要返回支付宝网关
            ali_pay_url = order_string if is_app_pay(order_string) else gatway + "?" + order_string

            # return JsonResponse(dict(ali_pay_url=ali_pay_url))

            res = {
                'err': 0,
                'msg': 'OK',
                'data': {
                    'ali_pay_url': ali_pay_url,
                },
            }
        # return JsonResponse(dict(ali_pay_url=""))
        return JsonResponse(res)

    @csrf_exempt
    def pay_result(self):
        """
        支付完成后，前端同步通知回调
        :param request:
        :return: 根据业务需求自定义返回信息
        """
        if self.method == "GET":
            data = self.GET.dict()
            # 同步验签data参数转换字典后示例如下：
            """
            {
                'charset': 'utf-8', 
                'out_trade_no': '20200808154711123456', 
                'method': 'alipay.trade.page.pay.return', 
                'total_amount': '0.01', 
                'sign': 'OBCdRRpUHtjAR15v9s26cU1juP+ub0COKRe3hJg2kCsMZIhCT3Kx......meYt0G2Kir/Ld77gp+OFLza2G5HrIrA==', 
                'trade_no': '2020080622001460481437011111', 
                'auth_app_id': '2016101000655892', 
                'version': '1.0', 
                'app_id': '2016101000655892', 
                'sign_type': 'RSA2', 
                'seller_id': '2078131328364326', 
                'timestamp': '2020-08-06 14:47:25'
            }
            """
            ali_pay = my_ali_pay()
            sign = data.pop('sign', None)
            success = ali_pay.verify(data, sign)
            # print("同步回调验签状态: ", success)
            if success:
                # 此处写支付验签成功的相关业务逻辑
                return JsonResponse(dict(message="支付成功"))

            return JsonResponse(dict(message="支付失败"))

        return JsonResponse(dict(message="支付失败"))

    # @csrf_exempt
    # @atomic()
    def update_order(self):
        """
        支付成功后，支付宝服务器异步通知回调（用于修改订单状态）
        :param request:
        :return: success or fail
        """
        if self.method == "POST":
            print("异步通知验证开始")
            body_str = self.body.decode('utf-8')
            data = parse.parse_qs(body_str)
            # data = parse.parse_qs(parse.unquote(body))  # 回传的url中如果发现被编码，这里可以用unquote解码再转换成字典
            # 异步通知data参数转换字典后示例如下：
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
                callback_data['payment_status_id'] = 1
            elif data['trade_status'][0] == 'TRADE_CLOSED':
                callback_data['payment_status_id'] = 2
            elif data['trade_status'][0] == 'TRADE_SUCCESS':
                callback_data['payment_status_id'] = 3
            elif data['trade_status'][0] == 'TRADE_FINISHED':
                callback_data['payment_status_id'] = 4
            else:
                callback_data['payment_status_id'] = ''
            """
            {
                'auth_app_id': '2016101000655892', 
                'version': '1.0', 
                'charset': 'utf-8', 
                'subject': '产品名称-20200808154711123456', 
                'trade_status': 'TRADE_SUCCESS', 
                'app_id': '2016101000655892', 
                'total_amount': '0.01', 
                'buyer_pay_amount': '0.01', 
                'receipt_amount': '0.01', 
                'point_amount': '0.00', 
                'invoice_amount': '0.01', 
                'trade_no': '2020080622001460481436956490', 
                'sign_type': 'RSA2', 
                'buyer_id': '2083402614260483', 
                'notify_time': '2020-08-06 12:38:06', 
                'notify_id': '2020080600125143806060481455916209', 
                'notify_type': 'trade_status_sync', 
                'fund_bill_list': '[{"amount":"0.01","fundChannel":"PCREDIT"}]', 
                'gmt_create': '2020-08-06 12:38:02', 
                'gmt_payment': '2020-08-06 12:38:06', 
                'seller_id': '2078131328364326', 
                'out_trade_no': '20200808154711123456', 
                'sign': 'YNeo9DqaKZzCLwN+7zYMCeYn6+pmo5fxCv/KtCWa8zBzNNKowRc23......iU30qCPFSzq/t4UtJ4TwA5/pfHo9cNlbKQA=='
            }
            """

            data = {k: v[0] for k, v in data.items()}

            ali_pay = my_ali_pay()
            sign = data.pop('sign', None)
            success = ali_pay.verify(data, sign)  # 返回验签结果, True/False
            print("异步通知验证状态: ", success)
            if success:
                # 此处写支付验签成功修改订单状态相关业务逻辑
                PaymentService.create(self, callback_data)
                return HttpResponse('success')  # 返回success给支付宝服务器, 若支付宝收不到success字符会重复发送通知
            return HttpResponse('fail')

        return HttpResponse('fail')

    @csrf_exempt
    def refund(self):
        """
         退款
        :param request:
        :return: success or fail
         """

        if self.method == "POST":
            # 根据当前用户的配置，生成URL，并跳转。
            # print(self)
            money = (self.POST.get('price'))
            out_trade_no = self.POST.get('out_trade_no')

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
            # 通知data参数转换字典后示例如下：
            """
            {
                "code": "10000",
                "msg": "Success",
                "buyer_logon_id": "jvg***@sandbox.com",
                "buyer_user_id": "2088622955554434",
                "fund_change": "Y",
                "gmt_refund_pay": "2022-08-10 14:01:02",
                "out_trade_no": "20220810054053350427",
                "refund_fee": "200.00",
                "send_back_fee": "0.00",
                "trade_no": "2022081022001454430501929100"
            }
            """
            # print(order_string)
            return JsonResponse(order_string)

    @csrf_exempt
    def close(self):
        if self.method == "POST":
            out_trade_no = self.POST.get('out_trade_no')
            trade_no = self.POST.get('trade_no')
            alipay = my_ali_pay()
            order_string = alipay.api_alipay_trade_close(
                out_trade_no=str(out_trade_no),
                trade_no=str(trade_no),
            )
            return JsonResponse(order_string)
