from pathlib import Path

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from main.settings import BASE_DIR
from xj_user.services.user_service import UserService
from xj_user.services.user_sso_serve_service import UserSsoServeService
from ..services.payment_wechat_service import PaymentWechatService
from ..services.payment_temporary_wechat_service import PaymentWechatService as temporary #为什么使用这个支付回调呢？？ 没有联动逻辑 答：支付已经整合 这个是为了刷单专门用的接口
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.model_handle import parse_data, util_response

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""


class PaymentWechat(APIView):
    # 获取唯一标识
    def get_user_info(self):
        code = self.GET.get('code', 0)
        wxpay_params = PaymentWechatService.get_user_info(code)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 小程序支付
    def payment_applets_pay(self):
        token = self.META.get('HTTP_AUTHORIZATION', None)
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            return util_response(err=6045, msg=error_text)
        sso_data, err = UserSsoServeService.user_sso_to_user(token_serv['user_id'], sub_appid)
        if err:
            return util_response(err=6045, msg="单点登录记录不存在")
        sso_data = model_to_dict(sso_data)
        params = parse_data(self)
        params['openid'] = sso_data['sso_unicode']
        wxpay_params = temporary.payment_applets_pay(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 扫码支付
    def payment_scan_pay(self):
        params = parse_data(self)
        wxpay_params = PaymentWechatService.payment_scan_pay(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 微信小程序红包
    def payment_red_envelopes(self):
        params = parse_data(self)
        wxpay_params = PaymentWechatService.payment_red_envelopes(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': wxpay_params
        })

    # 回调接口
    def callback(self):
        body = self.body
        wxpay_params = PaymentWechatService.callback_old(body)
        return HttpResponse(wxpay_params)

    # 回调接口 v3
    def callback_v3(self):
        body = self.body
        headers = {}

        headers.update({'Wechatpay-Signature': self.META.get('HTTP_WECHATPAY_SIGNATURE', "")})
        headers.update({'Wechatpay-Timestamp': self.META.get('HTTP_WECHATPAY_TIMESTAMP', "")})
        headers.update({'Wechatpay-Nonce': self.META.get('HTTP_WECHATPAY_NONCE', "")})
        headers.update({'Wechatpay-Serial': self.META.get('HTTP_WECHATPAY_SERIAL', "")})
        wxpay_params = PaymentWechatService.callback(headers, body)
        return JsonResponse(wxpay_params)
