# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 13:51:10
@LastEditTime: 2022-11-25 09:59:01
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.mp_base_model import *
from seven_cloudapp_frame.models.push_base_model import *
from asq.initiators import query
from seven_cloudapp_frame.libs.customize.baidubce_helper import *

class AppExpireHandler(ClientBaseHandler):
    """
    :description: 获取小程序是否过期未续费
    """
    def get_async(self):
        """
        :description: 获取小程序是否过期未续费
        :return info
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()

        app_base_model = AppBaseModel(context=self)
        invoke_result_data = app_base_model.get_app_expire(app_id)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(self.business_process_executed(invoke_result_data.data, ref_params={}))


class CreateWeChatQrCodeHandler(ClientBaseHandler):
    """
    :description: 创建微信小程序码
    """
    def get_async(self):
        """
        :description: 创建微信小程序码
        :param page：跳转地址
        :param scene：参数，不限制小程序码才支持
        :param env_version：要打开的小程序版本。正式版为 "release"，体验版为 "trial"，开发版为 "develop"。默认是正式版。不限制小程序码才支持
        :param width：宽度
        :param no_limit_code：是否不限制小程序码（1-是0否）
        :return: 二进制流
        :last_editors: HuangJianYi
        """
        page = self.get_param("page", "pages/index/index")
        scene = self.get_param("scene", "a=1")
        width = self.get_param_int("width", 430)
        env_version = self.get_param("env_version", "release")
        no_limit_code = self.get_param_int("no_limit_code", 1)
        if no_limit_code == 1:
            invoke_result_data = WeChatHelper.create_qr_code_unlimit(page=page, scene=scene, width=width, env_version=env_version)
        else:
            invoke_result_data = WeChatHelper.create_qr_code(path=page, width=width)
        self.set_header("Content-type", "image/png")
        if invoke_result_data.success == True:
            self.write(invoke_result_data.data)
        else:
            self.write("")


class UploadFileHandler(ClientBaseHandler):
    """
    :description: 上传文件
    """

    def get_async(self):
        """
        :description: 上传文件
        :last_editors: HuangJianYi
        """
        # 上传图片到资源服务器
        if not self.request.files:
            return self.response_json_error("error", "未获取到文件")

        file_path = BaidubceHelper.upload_file(self.request.files, context=self)
        if not file_path:
            return self.response_json_error("error", "上传文件失败")
        return self.response_json_success(file_path)


class AddWechatSubscribeHandler(ClientBaseHandler):
    """
    :description: 添加微信订阅次数
    """
    def get_async(self):
        """
        :description: 添加微信订阅次数
        :param template_id：template_id
        :param open_id：open_id
        :return: 
        :last_editors: HuangJianYi
        """
        template_id = self.get_param("template_id")
        open_id = self.get_param("open_id")
        push_base_model = PushBaseModel(context=self)
        invoke_result_data = push_base_model.add_wechat_subscribe(config.get_value("app_id"), template_id, open_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class GetHighPowerListHandler(ClientBaseHandler):
    """
    :description: 获取中台配置的高级权限列表
    """
    def get_async(self):
        """
        :description: 获取中台配置的高级权限列表
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        app_base_model = AppBaseModel(context=self)
        app_info_dict = app_base_model.get_app_info_dict(app_id)
        if not app_info_dict:
            return self.response_json_error("Error", "小程序不存在")
        store_user_nick = app_info_dict["store_user_nick"]
        access_token = app_info_dict["access_token"]
        config_data = {}
        config_data["is_customized"] = 0
        top_base_model = TopBaseModel(context=self)
        mp_base_model = MPBaseModel(context=self)
        custom_function_list = mp_base_model.get_custom_function_list(store_user_nick)
        if len(custom_function_list) == 0:
            app_key, app_secret = self.get_app_key_secret()
            #获取项目编码
            project_code = top_base_model.get_project_code(store_user_nick, access_token, app_key, app_secret)
            public_function_list = mp_base_model.get_public_function_list(project_code)
            if len(public_function_list) > 0:
                config_data["function_config_list"] = query(public_function_list[0]["function_info_second_list"]).select(lambda x: {"name": x["name"], "key_name": x["key_name"]}).to_list()
        else:
            config_data["is_customized"] = 1
            config_data["function_config_list"] = []
            custom_function_list = list(filter(lambda custom_function: custom_function["app_id"] == app_id, custom_function_list))
            if len(custom_function_list) > 0:
                config_data["function_config_list"] = query(custom_function_list[0]["function_info_second_list"]).select(lambda x: {"name": x["name"], "key_name": x["key_name"]}).to_list()
        self.response_json_success(self.business_process_executed(config_data, ref_params={}))
