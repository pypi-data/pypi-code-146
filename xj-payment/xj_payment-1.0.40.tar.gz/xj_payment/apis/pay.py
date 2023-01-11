#!/usr/bin/python3
import os
import requests
import json
import logging
# from __future__ import absolute_import
from datetime import datetime, timedelta
from pathlib import Path

from django.http import JsonResponse

from main.settings import BASE_DIR
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.base import WechatPayDALBase

pay_logger = logging.getLogger('pay')

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""

sub_app_secret = main_config_dict.wechat_merchant_app_secret or module_config_dict.wechat_merchant_app_secret or ""

sub_mch_id = main_config_dict.wechat_merchant_mch_id or module_config_dict.wechat_merchant_mch_id or ""

apiv3_secret = main_config_dict.wechat_apiv3_secret or module_config_dict.wechat_apiv3_secret or ""

trade_type = main_config_dict.wechat_trade_type or module_config_dict.wechat_trade_type or ""
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

# 商户证书序列号
serial_no = '548FB2EFC2CBBA142124DB82AED2B539977B062E.'

class WechatPayDAL(WechatPayDALBase):
    def get_official_cert(self):
        '''
        获取微信更新证书并保存
        '''
        url = 'https://api.mch.weixin.qq.com/v3/certificates'
        headers = self.make_headers_v3(url)
        rsp = requests.get(url, headers=headers)
        pay_logger.info('rsp:{}|{}'.format(rsp.status_code, rsp.content))
        rdct = rsp.json()
        for info in rdct['data']:
            ret = self.decrypt_v3(info)
            fpath = 'wechat_official_cert_{}.pem'.format(info['serial_no'])
            with open(fpath, 'wb') as ofile:
                ofile.write(ret)

        return fpath

    def create_order_info(self):
        '''
        创建微信预支付订单, 注意包含两次签名过程:
        首次签名用于请求微信后端获取prepay_id
        二次签名信息返回客户端用于调起SDK支付
        '''
        wechat = WechatPayDALBase(
            mch_appid=sub_mch_id,
            mchid=sub_appid,
            v3key=apiv3_secret,
            serial_no=serial_no,
            client_key=private_key_path
        )
        url = 'https://api.mch.weixin.qq.com/v3/pay/partner/transactions/jsapi'
        ndt = datetime.now()
        out_trade_no = self.generate_partner_trade_no(ndt)
        data = {
            'mchid': sub_mch_id,
            'out_trade_no': out_trade_no,
            'appid': sub_appid,
            'description': description,
            'notify_url': notify_url,
            'amount': {
                'currency': 'CNY',
                'total': int(total_fee),
            },
            'time_expire': (ndt + timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S+08:00')
        }
        jdata = json.dumps(data, separators=[',', ':'])
        headers = {'Content-Type': 'application/json'}
        # 第一次签名, 直接请求微信后端
        headers = wechat.make_headers_v3(url, headers=headers, body=jdata, method='POST')
        rsp = requests.post(url, headers=headers, data=jdata)
        pay_logger.info('rsp:{}|{}'.format(rsp.status_code, rsp.text))
        rdct = rsp.json()
        print(rdct)
        # 第二次签名, 返回给客户端调用
        sign_info = wechat.get_pay_sign_info(rdct['prepay_id'])

        return JsonResponse(sign_info)
        # return sign_info

    def query_order(self, out_trade_no):
        '''
        查询指定订单信息
        '''
        url = f'https://api.mch.weixin.qq.com/v3/pay/transactions/out-trade-no/{out_trade_no}?mchid={self.mchid}'
        headers = self.make_headers_v3(url)
        rsp = requests.get(url, headers=headers)
        pay_logger.info('out_trade_no:{}, rsp:{}|{}'.format(out_trade_no, rsp.status_code, rsp.text))
        rdct = rsp.json()
        return rdct
