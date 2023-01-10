# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-11-17 18:51:25
@LastEditTime: 2022-11-21 17:01:14
@LastEditors: HuangJianYi
@Description: 
"""
import hashlib
from seven_framework import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bos.bos_client import BosClient
from baidubce.services.bos import storage_class

class BaidubceHelper:
    """
    :description: 百度云帮助类
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_access_token(self):
        """
        :description:动态获取access_token
        :return: 
        :last_editors: HuangJianYi
        """
        api_key = config.get_value("baidubce_config", {}).get("text_censor",{}).get("api_key","")
        secret_key = config.get_value("baidubce_config", {}).get("text_censor", {}).get("secret_key","")
        request_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'
        response = requests.get(request_url)
        if response:
            if "error" not in json.loads(response.text).keys():
                access_token = json.loads(response.text)["access_token"]
                redis_init = SevenHelper.redis_init(config_dict=config.get_value("platform_redis"))
                redis_init.set("baidu_access_token", access_token, ex=2591000)
                return access_token
            else:
                self.logger_error("【获取百度云access_token失败】" + response.text)
        return ""

    @classmethod
    def text_censor(self, text, conclusion_types = [1]):
        """
        :description: 百度云文本审核
        :param text：内容
        :param conclusion_types：允许审核通过的结果类型（1.合规，2.不合规，3.疑似，4.审核失败）
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        access_token = SevenHelper.redis_init().get("baidu_access_token")
        if not access_token:
            access_token = self.get_access_token()
        if not access_token:
            invoke_result_data.success = False
            invoke_result_data.error_code = "fail_access_token"
            invoke_result_data.error_message = "无法进行文本审核"
            return invoke_result_data
        params = {"text": text}
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            if "error_code" not in json.loads(response.text).keys():
                conclusion_type = response.json()["conclusionType"]
                if conclusion_type not in  conclusion_types:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "fail"
                    invoke_result_data.error_message = "存在敏感词"
                    return invoke_result_data
                invoke_result_data.data = conclusion_type
                return invoke_result_data
            else:
                self.logger_error("【百度云文本审核失败】" + response.text)
        invoke_result_data.success = False
        invoke_result_data.error_code = "fail"
        invoke_result_data.error_message = "无法进行文本审核"
        return invoke_result_data

    @classmethod
    def get_bos_client(self):
        """
        :description: 获取百度云存储对象的client客户端
        """
        baidubce_config = config.get_value("baidubce_config", {}).get("bos", {})
        access_key = baidubce_config.get("access_key", "")
        secret_key = baidubce_config.get("secret_key", "")
        end_point = baidubce_config.get("end_point", "")
        # 创建认证组
        credentials = BceCredentials(access_key_id=access_key, secret_access_key=secret_key)
        # 创建BceClientConfiguration
        config = BceClientConfiguration(credentials=credentials, endpoint=end_point)
        # 获取到客户端
        bos_client = BosClient(config=config)
        return bos_client

    @classmethod
    def context_md5(self, stream):
        md5 = hashlib.md5()
        md5.update(stream)
        content_md5 = base64.standard_b64encode(md5.digest())
        return content_md5

    @classmethod
    def put_object(self, file_name, stream):
        """
        :description:根据文件名上传到服务器
        :param file_name: 文件名
        :param stream: 二进制流
        :return: 
        :last_editors: HuangJianYi
        """
        bos_client = self.get_bos_client()
        baidubce_config = config.get_value("baidubce_config", {}).get("bos", {})
        folder = baidubce_config.get("folder", "")
        bucket = baidubce_config.get("bucket", "")
        domain = baidubce_config.get("domain", "")
        object_key = folder + "/" + str(int(time.time())) + str(uuid.uuid4()) + file_name
        # 根据文件名上传文件
        try:
            result = bos_client.put_object(bucket_name=bucket, key=object_key, data=stream, content_length=len(stream), content_md5=self.context_md5(stream), storage_class=storage_class.STANDARD)
            if result:
                return domain + "/" + object_key
        except Exception as e:
            self.logger_error("【上传文件出错】" + str(traceback.format_exc()))
        return ""

    @classmethod
    def upload_file(self, reqeust_file: dict):
        """
        :description:上传文件
        :param reqeust_file: 请求文件字典
        :return: 
        :last_editors: HuangJianYi
        """
        files = reqeust_file.get("file")
        # 只上传一个文件
        item = files[0]
        filename = item.get("filename")
        filebody = item.get("body")
        return self.put_object(filename, filebody)
