import ast
import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.cache import cache
from rest_framework import response
from rest_framework.views import APIView

from config.config import Config

# from utils import restful

config = Config()
accesskey_id = config.get("xj_user", "ACCESSKEY_ID", "")
accesskey_secret = config.get("xj_user", "ACCESSKEY_SECRET", "")
sign_name = config.get("xj_user", "SIGN_NAME", "")
template_code = config.get("xj_user", "TEMPLATE_CODE", "")


class UserShortMessage(APIView):

    def post(self, request):
        if not accesskey_id or not accesskey_secret or not sign_name or not template_code:
            res = {
                'err': 4999,
                'msg': "短信参数未配置"
            }
            return response.Response(res)

        # http://localhost:8000/duanxin/duanxin/sms_send/?phone=18434288349
        # 1 获取手机号
        phone = request.POST.get('phone')
        # 2 生成6位验证码
        code = self.get_code(6, False)
        # print(code)
        # 3 缓存到Redis
        cache.set(phone, code, 300)  # 60s有效期
        # print('判断缓存中是否有:', cache.has_key(phone))
        # print('获取Redis验证码:', cache.get(phone))
        # 4 发短信
        result = self.send_sms(phone, code)
        dictionary = ast.literal_eval(result)
        if dictionary['Code'] == 'OK':
            res = {
                'err': 0,
                'msg': 'OK'
            }
        else:
            res = {
                'err': 4999,
                'msg': dictionary['Message']
            }

        return response.Response(res)

    def send_sms(self, phone, code):
        client = AcsClient(accesskey_id, accesskey_secret)
        code = "{'code':%s}" % (code)
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')  # url
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('PhoneNumbers', phone)  # 待发送手机号
        request.add_query_param('SignName', sign_name)  # 短信签名
        request.add_query_param('TemplateCode', template_code)  # 短信模板code
        request.add_query_param('TemplateParam', code)
        response = client.do_action_with_exception(request)
        # python2: print(response)
        return str(response, encoding='utf-8')

    # 数字表示生成几位, True表示生成带有字母的 False不带字母的
    def get_code(self, n=6, alpha=False):
        s = ''  # 创建字符串变量,存储生成的验证码
        for i in range(n):  # 通过for循环控制验证码位数
            num = random.randint(0, 9)  # 生成随机数字0-9
            if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
                upper_alpha = chr(random.randint(65, 90))
                lower_alpha = chr(random.randint(97, 122))
                num = random.choice([num, upper_alpha, lower_alpha])
            s = s + str(num)
        return s
