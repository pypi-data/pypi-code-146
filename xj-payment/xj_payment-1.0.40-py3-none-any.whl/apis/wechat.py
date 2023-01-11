import json
import os
import time
from random import sample
from string import ascii_letters, digits
import logging
from pathlib import Path

from celery.utils.serialization import jsonify

from main.settings import BASE_DIR
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from wechatpayv3 import SignType, WeChatPay, WeChatPayType
from ..services.payment_wechat_service import PaymentWechatService

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

app_id = main_config_dict.wechat_service_app_id or module_config_dict.wechat_service_app_id or ""

app_secret = main_config_dict.wechat_service_app_secret or module_config_dict.wechat_service_app_secret or ""

mch_id = main_config_dict.wechat_service_mch_id or module_config_dict.wechat_service_mch_id or ""

merchant_key = main_config_dict.wechat_service_merchant_key or module_config_dict.wechat_service_merchant_key or ""

sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""

sub_app_secret = main_config_dict.wechat_merchant_app_secret or module_config_dict.wechat_merchant_app_secret or ""

sub_mch_id = main_config_dict.wechat_merchant_mch_id or module_config_dict.wechat_merchant_mch_id or ""

apiv3_secret = main_config_dict.wechat_apiv3_secret or module_config_dict.wechat_apiv3_secret or ""

trade_type = main_config_dict.wechat_trade_type or module_config_dict.wechat_trade_type or ""

cert_serial_no = main_config_dict.wechat_cert_serial_no or module_config_dict.wechat_cert_serial_no or ""

cert_dir = main_config_dict.wechat_cert_dir or module_config_dict.wechat_cert_dir or ""
# 交易类型，小程序取值：JSAPI

# 商品描述，商品简单描述
description = main_config_dict.wechat_body or module_config_dict.wechat_body or ""
# 标价金额，订单总金额，单位为分
total_fee = main_config_dict.wechat_total_fee or module_config_dict.wechat_total_fee or ""
# 通知地址，异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
notify_url = main_config_dict.wechat_notify_url or module_config_dict.wechat_notify_url or ""

private_key_path = main_config_dict.wechat_merchant_private_key_file or module_config_dict.wechat_merchant_private_key_file or (
        str(BASE_DIR) + "/config/apiclient_key.pem")
# 读取文件获取密钥
private_key = open(private_key_path, encoding="utf-8").read() if os.path.exists(private_key_path) else ""

# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
MCHID = mch_id

# 商户证书私钥
# with open('path_to_key/apiclient_key.pem') as f:
#     PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = cert_serial_no

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = apiv3_secret

# APPID，应用ID或服务商模式下的sp_appid
APPID = app_id

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = notify_url

# 微信支付平台证书缓存目录，减少证书下载调用次数
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
CERT_DIR = cert_dir

# 日志记录器，记录web请求和回调细节
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")

# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = True

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None


class WeChatPayment(APIView):
    def pay(self):
        # jsapi下单，wxpay初始化的时候，wechatpay_type设置为WeChatPayType.JSAPI。
        # 下单成功后，将prepay_id和其他必须的参数组合传递给JSSDK的wx.chooseWXPay接口唤起支付
        wxpay = WeChatPay(
            wechatpay_type=WeChatPayType.JSAPI,
            mchid=mch_id,
            private_key=private_key,
            cert_serial_no=CERT_SERIAL_NO,
            apiv3_key=APIV3_KEY,
            appid=app_id,
            notify_url=NOTIFY_URL,
            cert_dir=CERT_DIR,
            logger=LOGGER,
            partner_mode=PARTNER_MODE,
            proxy=PROXY)

        out_trade_no = ''.join(sample(ascii_letters + digits, 8))
        description = 'demo-description'
        amount = 1
        # payer = {'openid': 'oj8KR5AR0sV20j96VBcnWulf7bbs'}
        # payer = json.dumps(payer)
        code, message = wxpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            sub_appid=sub_appid,
            sub_mchid=sub_mch_id,
            amount={'total': amount},
            payer={'sub_openid': 'oj8KR5AR0sV20j96VBcnWulf7bbs'}
        )
        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get('prepay_id')
            timestamp = PaymentWechatService.to_text(int(time.time()))
            noncestr = PaymentWechatService.random_string(32)
            package = 'prepay_id=' + prepay_id
            paysign = wxpay.sign([sub_appid, timestamp, noncestr, package])
            signtype = 'RSA'
            return JsonResponse({'code': 0, 'result': {
                'appId': sub_appid,
                'timeStamp': timestamp,
                'nonceStr': noncestr,
                'package': 'prepay_id=%s' % prepay_id,
                'signType': signtype,
                'paySign': paysign
            }})
        else:
            return JsonResponse({'code': -1, 'result': {'reason': result.get('code')}})
