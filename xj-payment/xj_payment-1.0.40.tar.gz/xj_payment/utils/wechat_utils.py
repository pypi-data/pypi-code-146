import os
import random
import string
import hashlib
import OpenSSL
import requests
import six
from datetime import datetime
import logging
from pathlib import Path
from wechatpy import WeChatPay
from wechatpy.pay.utils import get_external_ip
from wechatpayv3 import SignType, WeChatPay as WeChatPay3, WeChatPayType
from main.settings import BASE_DIR
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
# APPID，应用ID或服务商模式下的sp_appid
app_id = main_config_dict.wechat_service_app_id or module_config_dict.wechat_service_app_id or ""
# 商户号（服务号）
mch_id = main_config_dict.wechat_service_mch_id or module_config_dict.wechat_service_mch_id or ""
# 小程序SECRET （服务号）
app_secret = main_config_dict.wechat_service_app_secret or module_config_dict.wechat_service_app_secret or ""
# 商户KEY（服务号）
merchant_key = main_config_dict.wechat_service_merchant_key or module_config_dict.wechat_service_merchant_key or ""
# 小程序ID（子商户）
sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""
# 小程序SECRET （子商户）
sub_app_secret = main_config_dict.wechat_merchant_app_secret or module_config_dict.wechat_merchant_app_secret or ""
# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
sub_mch_id = main_config_dict.wechat_merchant_mch_id or module_config_dict.wechat_merchant_mch_id or ""
# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
apiv3_secret = main_config_dict.wechat_apiv3_secret or module_config_dict.wechat_apiv3_secret or ""
# 商户证书序列号
cert_serial_no = main_config_dict.wechat_cert_serial_no or module_config_dict.wechat_cert_serial_no or ""
# 微信支付平台证书缓存目录，减少证书下载调用次数
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
cert_dir = main_config_dict.wechat_cert_dir or module_config_dict.wechat_cert_dir or ""
# 商品描述，商品简单描述
description = main_config_dict.wechat_body or module_config_dict.wechat_body or ""
# 商户名称
merchant_name = main_config_dict.merchant_name or module_config_dict.merchant_name or ""
# 标价金额，订单总金额，单位为分
total_fee = main_config_dict.wechat_total_fee or module_config_dict.wechat_total_fee or ""
# 通知地址，异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。回调地址，也可以在调用接口的时候覆盖
notify_url = main_config_dict.wechat_notify_url or module_config_dict.wechat_notify_url or ""
# 商户证书私钥路径
private_key_path = main_config_dict.wechat_merchant_private_key_file or module_config_dict.wechat_merchant_private_key_file or (
        str(BASE_DIR) + "/config/cert/apiclient_key.pem")
# 商户证书
cert_path = main_config_dict.wechat_merchant_cert_file or module_config_dict.wechat_merchant_cert_file or (
        str(BASE_DIR) + "/config/cert/apiclient_cert.pem")

# 商户证书私钥路径
son_private_key_path = main_config_dict.wechat_son_merchant_private_key_file or module_config_dict.wechat_son_merchant_private_key_file or (
        str(BASE_DIR) + "/config/cert/son/apiclient_key.pem")
# 商户证书
son_cert_path = main_config_dict.wechat_son_merchant_cert_file or module_config_dict.wechat_son_merchant_cert_file or (
        str(BASE_DIR) + "/config/cert/son/apiclient_cert.pem")

# 读取文件获取密钥
private_key = open(private_key_path, encoding="utf-8").read() if os.path.exists(private_key_path) else ""
# 日志记录器，记录web请求和回调细节
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")
# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = True
# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None
url = "https://api.mch.weixin.qq.com/v3/pay/partner/transactions/jsapi"
logger = logging.getLogger(__name__)


def my_ali_pay():
    wechat = WeChatPay(
        appid=app_id,
        sub_appid=sub_appid,
        api_key=merchant_key,
        mch_id=mch_id,
        sub_mch_id=sub_mch_id,
        mch_key=apiv3_secret,
    )
    return wechat


def my_ali_pay_v3():
    wxpay = WeChatPay3(
        wechatpay_type=WeChatPayType.JSAPI,
        mchid=mch_id,
        private_key=private_key,
        cert_serial_no=cert_serial_no,
        apiv3_key=apiv3_secret,
        appid=app_id,
        notify_url=notify_url,
        cert_dir=cert_dir,
        logger=LOGGER,
        partner_mode=PARTNER_MODE,
        proxy=PROXY
    )
    return wxpay


def applets_red_envelopes():
    url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendminiprogramhb"
    # path = '/mmpaymkttransfers/sendminiprogramhb'
    now = datetime.now()
    out_trade_no = '{0}{1}{2}'.format(sub_mch_id, now.strftime('%Y%m%d%H%M%S'), random.randint(1000, 10000))
    data = {
        'nonce_str': random_string(32),
        'mch_billno': out_trade_no,  # 商户订单号
        'mch_id': mch_id,  # 商户号
        'wxappid': app_id,  # 公众账号appid
        'send_name': merchant_name,  # 商户名称
        're_openid': 'oj8KR5AR0sV20j96VBcnWulf7bbs',  # 用户openid
        'total_amount': 1,  # 付款金额
        'total_num': 1,  # 红包发放总人数
        'wishing': '恭喜发财',  # 红包祝福语
        'act_name': '余额提现',  # 活动名称
        'remark': '余额提现红包，请查收',  # 备注
        'notify_way': "MINI_PROGRAM_JSAPI",  # 通知用户形式
    }
    sign = calculate_signature(data, merchant_key)
    data['sign'] = sign
    body = dict_to_xml(data)
    amount = 1 / 100
    if amount >= 200:
        data['scene_id'] = 'PRODUCT_3'
    wx_key = os.path.join(private_key_path)
    wx_cert = os.path.join(cert_path)
    response = requests.post(url=url, data=body.encode('utf-8'),
                             cert=(wx_cert, wx_key))

    # response = requests.request("POST", url, headers=headers, data=body.encode("utf-8"))
    # response = requests.request("POST", url, data=body.encode('utf-8'), cert=(wx_cert, wx_key), verify=True)
    return response.text


def dict_to_xml(d, sign=None):
    xml = ['<xml>\n']
    for k in sorted(d):
        # use sorted to avoid test error on Py3k
        v = d[k]
        if isinstance(v, six.integer_types) or (isinstance(v, six.string_types) and v.isdigit()):
            xml.append('<{0}>{1}</{0}>\n'.format(to_text(k), to_text(v)))
        else:
            xml.append(
                '<{0}><![CDATA[{1}]]></{0}>\n'.format(to_text(k), to_text(v))
            )
    if sign:
        xml.append('<sign><![CDATA[{0}]]></sign>\n</xml>'.format(to_text(sign)))
    else:
        xml.append('</xml>')
    return ''.join(xml)


def format_url(params, api_key=None):
    data = [to_binary('{0}={1}'.format(k, params[k])) for k in sorted(params) if params[k]]
    if api_key:
        data.append(to_binary('key={0}'.format(api_key)))
    return b"&".join(data)


def calculate_signature(params, api_key):
    url = format_url(params, api_key)
    logger.debug("Calculate Signature URL: %s", url)
    return to_text(hashlib.md5(url).hexdigest().upper())


def to_binary(value, encoding='utf-8'):
    """Convert value to binary string, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return b''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return to_text(value).encode(encoding)


def random_string(length=16):
    rule = string.ascii_letters + string.digits
    rand_list = random.sample(rule, length)
    return ''.join(rand_list)


def to_text(value, encoding='utf-8'):
    """Convert value to unicode, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)
