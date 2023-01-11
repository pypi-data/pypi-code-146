# -*- coding: utf-8 -*-
import os
from pathlib import Path

from alipay import AliPay

from main.settings import BASE_DIR
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

# 当前模块路径
module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=module_root + "/config.ini", section="xj_payment"))
# 密钥地址
private_key_path = main_config_dict.APP_PRIVATE_KEY_FILE or module_config_dict.APP_PRIVATE_KEY_FILE or (str(BASE_DIR) + "/config/app_private_key.pem")
public_key_path = main_config_dict.ALIPAY_PUBLIC_KEY_FILE or module_config_dict.ALIPAY_PUBLIC_KEY_FILE or (str(BASE_DIR) + "/config/alipay_public_key.pem")
# 读取文件获取密钥
private_key = open(private_key_path, encoding="utf-8").read() if os.path.exists(private_key_path) else ""
public_key = open(public_key_path, encoding="utf-8").read() if os.path.exists(public_key_path) else ""
app_id = main_config_dict.alipay_app_id or module_config_dict.alipay_app_id or ""

def my_ali_pay(notify_url=None):
    """
    支付宝支付对象
    :param notify_url:
    支付成功支付宝服务器异步通知默认回调url，会向这个地址发送POST请求，接口实现校验是否支付已经完成，注意：此地址需要能在公网进行访问
    :return: 支付对象
    """

    alipay = AliPay(
        appid=app_id,
        # appid=settings.ALIPAY_APP_ID,  # APPID
        app_notify_url=notify_url,  # 默认回调url,可以传也可以不传
        # app_notify_url=notify_url,  # 默认回调url,可以传也可以不传
        app_private_key_string=private_key,
        # app_private_key_string=settings.APP_PRIVATE_KEY,  # 应用私钥
        # alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY,  # 支付宝公钥
        alipay_public_key_string=public_key,
        sign_type="RSA2",  # RSA 或者 RSA2
        # debug=settings.ALI_PAY_DEBUG  # 默认False，沙箱环境改成True
        debug=True
    )

    return alipay


def is_app_pay(order_string):
    """
    判断是否是App支付
    :param order_string: 签名后的订单信息
    :return: True or False
    支付宝支付功能对应的方法:
    注意: App支付不需要传支付网关ALI_PAY_URL
    电脑网站支付: alipay.trade.page.pay
    手机网站支付: alipay.trade.wap.pay
    App支付: alipay.trade.app.pay
    小程序支付: alipay.trade.create
    当面付(条码支付): alipay.trade.pay
    交易预创建(扫码支付): alipay.trade.precreate
    """
    order_dict = dict()
    for i in order_string.split('&'):
        temp_list = i.split("=")
        order_dict[temp_list[0]] = temp_list[1]

    method = order_dict.get("method")

    return True if "app" in method else False
