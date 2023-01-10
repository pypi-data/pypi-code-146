# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 14:03:12
@LastEditTime: 2023-01-04 15:53:26
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.enum import PageCountMode
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.act_base_model import *
from seven_cloudapp_frame.models.cms_base_model import *
from seven_cloudapp_frame.models.prize_base_model import *
from seven_cloudapp_frame.models.price_base_model import *


class ActInfoHandler(ClientBaseHandler):
    """
    :description: 获取活动信息
    """
    def get_async(self):
        """
        :description: 获取活动信息
        :param act_id：活动标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        app_base_model = AppBaseModel(context=self)
        act_base_model = ActBaseModel(context=self)
        app_info_dict = app_base_model.get_app_info_dict(app_id)
        if not app_info_dict:
            return self.response_json_error("error", "小程序不存在")
        act_info_dict = act_base_model.get_act_info_dict(act_id, True, False)
        if not act_info_dict:
            return self.response_json_error("error", "活动不存在")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        act_info_dict["seller_id"] = app_info_dict["seller_id"]
        act_info_dict["store_id"] = app_info_dict["store_id"]
        act_info_dict["store_name"] = app_info_dict["store_name"]
        act_info_dict["store_icon"] = app_info_dict["store_icon"]
        act_info_dict["app_icon"] = app_info_dict["app_icon"]

        act_info_dict = self.business_process_executed(act_info_dict, ref_params={})
        return self.response_json_success(act_info_dict)


class ActPrizeListHandler(ClientBaseHandler):
    """
    :description: 活动奖品列表
    """
    def get_async(self):
        """
        :description: 活动奖品列表
        :param act_id: 活动标识
        :param module_id: 活动模块标识
        :param prize_name: 奖品名称
        :param ascription_type: 奖品归属类型（0-活动奖品1-任务奖品）
        :param page_size: 条数
        :param page_index: 页数
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return: PageInfo
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = self.get_param_int("module_id", 0)
        prize_name = self.get_param("prize_name")
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 10)
        page_count_mode = self.get_param_int("page_count_mode", 1)

        if not app_id or not act_id:
            return self.response_json_success({"data": []})
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        prize_base_model = PrizeBaseModel(context=self)
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        page_list = prize_base_model.get_act_prize_list(app_id, act_id, module_id, prize_name, 0, 0, page_size, page_index, page_count_mode=page_count_mode)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)


class CmsInfoListHandler(ClientBaseHandler):
    """
    :description: 获取位置信息列表
    """
    @filter_check_params("place_id")
    def get_async(self):
        """
        :description: 获取位置信息列表
        :params place_id:位置标识
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        place_id = self.get_param_int("place_id", 0)
        page_size = self.get_param_int("page_size", 20)
        page_index = self.get_param_int("page_index", 0)
        page_count_mode = self.get_param_int("page_count_mode", 1)


        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "id desc"
        field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        cms_base_model = CmsBaseModel(context=self)
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        page_list = cms_base_model.get_cms_info_list(place_id=place_id, page_size=page_size, page_index=page_index, order_by=order_by, field=field, app_id=app_id, act_id=act_id, is_cache=True, page_count_mode=page_count_mode)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)


class PriceGearListHandler(ClientBaseHandler):
    """
    :description: 获取价格档位列表
    """
    def get_async(self):
        """
        :description: 获取价格档位列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param page_index：页索引
        :param page_size：页大小
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        page_size = self.get_param_int("page_size", 20)
        page_index = self.get_param_int("page_index", 0)
        page_count_mode = self.get_param_int("page_count_mode", 1)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc"
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        page_list = PriceBaseModel(context=self).get_price_gear_list(app_id, act_id, page_size, page_index, order_by, page_count_mode=page_count_mode)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)
