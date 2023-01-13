import os
import random
from datetime import time
from pathlib import Path

from django.http import HttpResponse

from ..utils.unionpay_utils import *

from main.settings import BASE_DIR
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
# 密钥地址
cert_path = main_config_dict.UNIONPAY_CERT_PATH or module_config_dict.UNIONPAY_CERT_PATH or (
        str(BASE_DIR) + "/config/acp_test_sign.pfx")

cert_password = main_config_dict.unionpay_cert_password

unionpay_version = main_config_dict.unionpay_version

# 商户ID(配置项)
unionpay_mer_id = main_config_dict.unionpay_mer_id

# 前台回调地址(支付成功回调成功)(配置项)（正式生产环境需修改）
unionpay_front_url = main_config_dict.unionpay_front_url

# 后台回调地址(配置项)（正式生产环境需修改）
unionpay_back_url = main_config_dict.unionpay_back_url

# 证书地址(配置项)（正式生产环境需修改）
unionpay_cert_path = main_config_dict.unionpay_cert_path

# 证书解密密码(根据实际去调配)(配置项) （正式生产环境需修改）
unionpay_cert_password = main_config_dict.unionpay_cert_password

# 是否开启测试模式(默认False)(配置项)（正式生产环境为False）
unionpay_debug = True

class PaymentUnionPayService:

    @staticmethod
    def get_uni_object():
        uni_pay = UnionPay(
            version=unionpay_version,
            mer_id=unionpay_front_url,
            front_url=unionpay_front_url,
            back_url=unionpay_back_url,
            backend_url=unionpay_cert_path,
            cert_path=cert_path,
            debug=unionpay_debug
        )
        return uni_pay

    # @staticmethod
    # 生成订单号（自定义）
    # def order_num(package_num, uid):
    #     '''
    #     商品代码后两位+下单时间后十二位+用户id后四位+随机数四位
    #     :param package_num: 商品代码
    #     :return: 唯一的订单号
    #     '''
    #     local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    #     result = str(package_num)[-2:] + local_time + uid[-4:] + str(random.randint(1000, 9999))
    #     return result


    # 账户充值（银联）  # uid参数可不传入，此处用于生成订单号
    @staticmethod
    def unipay(money, uid):
        # money = float(request.POST.get('money'))
        unipay = PaymentUnionPayService.get_uni_object()
        query_params = unipay.build_request_data(
            order_id="123456",  # 用户购买订单（每次不一样）
            txn_amt=int(float(money) * 100)  # 交易金额 单位分
        )
        # pay_html = unipay.pay_html(query_params)
        # rsp = HttpResponse()
        # rsp.content = pay_html
        return query_params


    # 充值成功后前台回调(银联)
    @staticmethod
    def uni_back(request, uid):
        if request.method == "POST":
            params = request.POST.dict()
            unipay = PaymentUnionPayService.get_uni_object(uid)
            res = unipay.verify_sign(params)
            if res:
                if unipay.verify_query(params['orderId'], params['txnTime']):  # 再次查询状态
                    return HttpResponse('充值成功')
            else:
                return HttpResponse('充值失败')


    # 充值成功后后台回调（银联）
    @staticmethod
    def uni_notify(request, uid):
        if request.method == "POST":
            params = request.POST.dict()
            unipay = PaymentUnionPayService.get_uni_object(uid)
            res = unipay.verify_sign(params)
            if res:
                status = unipay.verify_query(params['orderId'], params['txnTime'])  # 再次查询状态
                if status:
                    try:
                        # updata_data(uid, float(int(params['txnAmt']) / 100))
                        return HttpResponse('ok')
                    except Exception as e:
                        raise e
            else:
                return None, None
        else:
            params = request.GET.dict()
            for k, v in params.items():
                print(k, v, '\n')
        return HttpResponse('failed')
