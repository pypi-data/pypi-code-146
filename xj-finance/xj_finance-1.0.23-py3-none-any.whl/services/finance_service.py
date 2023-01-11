import time
import os
import datetime

from django.db.models import Q
from django.db.models import F
from django.forms import model_to_dict
from xj_user.services.user_platform_service import UserPlatformService
from ..models import *

from decimal import Decimal
from ..utils.custom_tool import format_params_handle


class FinanceService:

    def __init__(self):
        pass

    # 检查账号余额是否正确
    @staticmethod
    def check_balance(account_id='', platform='', platform_id=None, currency='', sand_box=''):
        # print("-" * 30, os.path.basename(__file__), "-" * 30)
        # print("check_balance account_id, platform, currency:", account_id, platform, currency, )

        # ========== 一、内容的类型准确性检查 ==========
        account_set = BaseInfo.objects.filter(id=account_id).first()
        if not account_set:
            # print('check_balance: account_id不存在', account_id, account_set)
            return {'err': 7001, 'msg': 'check_balance: account_id不存在:' + str(account_id)}

        # platform_set = Platform.objects.filter(platform_name=platform).first()
        if platform:
            platform_info, error = UserPlatformService.get_platform_info(platform_name=platform)
            if error:
                # print('check_balance: platform不存在', platform, platform_info)
                return {'err': 7002, 'msg': 'check_balance: platform不存在' + str(platform)}
            platform_id = platform_info.get('platform_id')

        currency_set = Currency.objects.filter(currency=currency).first()
        if not currency_set:
            # print('check_balance: currency不存在', currency, currency_set)
            return {'err': 7003, 'msg': 'check_balance: currency不存在' + str(currency)}

        sand_box = sand_box if sand_box else None
        sand_box_set = None
        if sand_box:
            sand_box_set = SandBox.objects.filter(sand_box_name=sand_box).first()
        if sand_box and not sand_box_set:
            # print('check_balance: sand_box不存在', sand_box, sand_box_set)
            return {'err': 7004, 'msg': 'check_balance: sand_box不存在' + str(sand_box)}

        # ========== 二、相关前置业务逻辑处理 ==========
        transact_set = Transact.objects.filter(
            Q(account_id=account_id) &
            Q(platform_id=platform_id) &
            Q(currency__currency=currency)
        )

        if sand_box is None:
            transact_set = transact_set.filter(Q(sand_box__sand_box_name__isnull=True))
        else:
            transact_set = transact_set.filter(Q(sand_box__sand_box_name=sand_box))

        transact_set = transact_set.order_by('transact_time')
        # print(">>> transact_set: ", transact_set)

        for i, it in enumerate(transact_set):
            is_inside_pay = True if str(it.pay_mode).upper() == 'BALANCE' else False
            # print(">>>>>> is_inside_pay:", is_inside_pay)
            income = it.income if it.income else Decimal(0.0)
            outgo = it.outgo if it.outgo else Decimal(0.0)
            # outgo = it.outgo if it.outgo and is_inside_pay else Decimal(0.0)

            # print('check_balance: for:', i, ': ', income, -outgo, ' = ', it.balance, )
            # print('check_balance: for:', i, type(income), type(outgo), type(it.balance))
            if is_inside_pay:
                if i == 0:
                    balance = income - outgo
                    # print(">>>>>> balance: ", balance)  # -10000.00000000
                    # print(">>>>>> it.balance: ", it.balance)  # 0E-8   0.00000000
                    if balance != it.balance:
                        # print('check_balance: 首条余额不匹配，自动修正:', i, income, -outgo, balance, it.balance)
                        it.balance = balance
                        it.save()
                    continue

                last = transact_set[i - 1]
                balance = last.balance + income - outgo
                if balance != it.balance:
                    # print('check_balance: 余额不匹配，自动修正:', i, last.balance, income, -outgo, balance, it.balance)
                    it.balance = balance
                    it.save()
        transact_set_new = Transact.objects.filter(
            Q(account_id=account_id) &
            Q(platform_id=platform_id) &
            Q(currency__currency=currency)
        )
        if sand_box is None:
            transact_set_new = transact_set_new.filter(Q(sand_box__sand_box_name__isnull=True))
        else:
            transact_set_new = transact_set_new.filter(Q(sand_box__sand_box_name=sand_box))
        transact_set_new = transact_set_new.order_by('-transact_time').first()
        transact_set_new = model_to_dict(transact_set_new)
        if transact_set_new:
            return {"balance": transact_set_new['balance']}
        return True

    # 生成交易号：2位数（当前年份后2位数字）+8位数（当前时间戳去头2位）+6位数（用户名 经过hash crc16生成的 4位十六进制 转成5位数 然后头为补0）
    @staticmethod
    def make_unicode(salt=''):
        # 当前时间戳
        date_time = time.localtime(time.time())
        # 截取第3位到第4位
        year_code = str(date_time.tm_year)[2:4]

        # 当前时间戳
        timestamp = str(int(time.time()))
        # 截取第3位到第10位
        timestamp_code = timestamp[2:10]

        # 十六进制校验码
        crc_hex = FinanceService.crc16(salt) if salt else '0'
        # 十六进制转十进制
        crc_int = int(crc_hex, 16)
        # 头位补0
        crc_code = str('000000' + str(crc_int))[-6:]
        unicode = year_code + timestamp_code + crc_code

        return unicode

    # crc16
    @staticmethod
    def crc16(x):
        a = 0xFFFF
        b = 0xA001
        for byte in x:
            a ^= ord(byte)
            for i in range(8):
                last = a % 2
                a >>= 1
                if last == 1:
                    a ^= b
        s = hex(a).upper()

        return s[2:6]

    @staticmethod
    def check_filter_validity(params={}):
        """
        检查过滤筛选的有效性函数
        :param params: 要检查的参数列表
        :return: 可用于查询的查询集
        """

        query_dict = {}

        # 搜索平台
        platform_name = params.get('platform', '')
        if platform_name:
            platform_set, err = UserPlatformService.get_platform_info(platform_name=platform_name)
            if err:
                return {'err': 3001, 'msg': 'platform不存在', }
            query_dict['platform_id'] = platform_set['platform_id']

        # 搜索币种
        currency = params.get('currency', '')
        if currency:
            currency_set = Currency.objects.filter(Q(currency=currency)).first()
            if not currency_set:
                return {'err': 3002, 'msg': 'currency不存在', }
            query_dict['currency__currency'] = currency

        # 搜索支付方式
        pay_mode = params.get('pay_mode', '')
        if pay_mode:
            pay_mode_set = PayMode.objects.filter(Q(pay_mode=pay_mode)).first()
            if not pay_mode_set:
                return {'err': 3003, 'msg': 'pay_mode不存在', }
            query_dict['pay_mode__pay_mode'] = pay_mode

        # 搜索沙盒
        sand_box = params.get('sand_box', '')
        # 如果沙盒为空则搜索全部内容，但沙盒为假值或者0时，则只显示非沙盒
        sand_box = False if sand_box.lower() == 'false' or sand_box == '0' else sand_box
        sand_box = True if sand_box.lower() == 'false' or sand_box == '0' else sand_box
        # 显示指定沙盒
        if sand_box and sand_box:
            sand_box_set = SandBox.objects.filter(Q(sand_box_name=sand_box)).first()
            if sand_box and not sand_box_set:
                return {'err': 3004, 'msg': 'sand_box不存在', }
            query_dict['sand_box__sand_box_name'] = sand_box
        # 显示非沙盒（即真实交易）
        if sand_box is False:
            query_dict['sand_box__sand_box_name__isnull'] = True

        # 模糊搜索对方账号
        their_account_name = params.get('their_account_name', '')
        if their_account_name:
            query_dict['their_account__full_name__icontains'] = their_account_name

        # 模糊搜索摘要search_word
        search_word = params.get('search_word', '')
        if search_word:
            query_dict['summary__icontains'] = search_word

        return {'err': 0, 'msg': 'OK', 'query_dict': query_dict, }

    #
    # # 过滤筛选
    # @staticmethod
    # def transact_filter(params={}, account_id=None, ):
    #     """
    #     :param params: 要过滤的参数列表
    #     :param obj_list:
    #     :return:
    #     """
    #
    #     transacts = Transact.objects.all()
    #
    #     # 是否只显示主账号的数据
    #     if account_id:
    #         transacts = transacts.filter(Q(account=account_id))
    #
    #     # 搜索平台
    #     platform_name = params.get('platform', '')
    #     print(">>> platform_name:", platform_name)
    #     if platform_name:
    #         platform_set = Platform.objects.filter(Q(platform_name=platform_name)).first()
    #         print(">>> platform_set:", platform_set)
    #         if not platform_set:
    #             return {'err': 3001, 'msg': 'platform不存在', }
    #         transacts = transacts.filter(Q(platform=platform_set.platform_id))
    #
    #     # 搜索币种
    #     currency = params.get('currency', '')
    #     if currency:
    #         currency_set = Currency.objects.filter(Q(currency=currency)).first()
    #         if not currency_set:
    #             return {'err': 3002, 'msg': 'currency不存在', }
    #         transacts = transacts.filter(Q(currency=currency_set.id))
    #
    #     # 搜索支付方式
    #     pay_mode = params.get('pay_mode', '')
    #     if pay_mode:
    #         pay_mode_set = PayMode.objects.filter(Q(pay_mode=pay_mode)).first()
    #         if not pay_mode_set:
    #             return {'err': 3003, 'msg': 'pay_mode不存在', }
    #         transacts = transacts.filter(Q(pay_mode=pay_mode_set.id))
    #
    #     # 搜索沙盒
    #     sand_box = params.get('sand_box', '')
    #     # 如果沙盒为空则搜索全部内容，但沙盒为假值或者0时，则只显示非沙盒
    #     sand_box = False if sand_box.lower() == 'false' or sand_box == '0' else sand_box
    #     # 显示指定沙盒
    #     if sand_box:
    #         sand_box_set = SandBox.objects.filter(Q(sand_box_name=sand_box)).first()
    #         if sand_box and not sand_box_set:
    #             return {'err': 3004, 'msg': 'sand_box不存在', }
    #         transacts = transacts.filter(Q(sand_box=sand_box_set.id))
    #     # 显示非沙盒（即真实交易）
    #     if sand_box is False:
    #         transacts = transacts.filter(Q(sand_box__sand_box_name__isnull=True))
    #
    #     # 模糊搜索对方账号
    #     their_account_name = params.get('their_account_name', '')
    #     if their_account_name:
    #         their_account_name_set = BaseInfo.objects.filter(Q(full_name__icontains=their_account_name)).values('id', 'full_name')
    #         query_str = ''
    #         for it in their_account_name_set:
    #             if query_str:
    #                 query_str += ' | Q(their_account=' + str(it['id']) + ')'
    #             else:
    #                 query_str += 'Q(their_account=' + str(it['id']) + ')'
    #         if not their_account_name_set:
    #             return {'err': 3005, 'msg': 'their_account_name不存在', }
    #         transacts = transacts.filter(eval(query_str))
    #
    #     # 模糊搜索摘要search_word
    #     search_word = params.get('search_word', '')
    #     if search_word:
    #         transacts = transacts.filter(Q(summary__icontains=search_word))
    #
    #     transacts = transacts.order_by('-transact_time')
    #
    #     return {'err': 0, 'msg': 'OK', 'query_set': transacts, }

