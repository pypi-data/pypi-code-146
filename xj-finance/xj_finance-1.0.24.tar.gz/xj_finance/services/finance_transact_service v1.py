import math
import random
import time
import os
from decimal import Decimal

import pytz
from django.db.models import Q
from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework import serializers

from xj_user.models import BaseInfo, Platform
from xj_user.services.user_platform_service import UserPlatformService

from ..utils.jt import Jt
from ..models import Transact, Currency, PayMode, SandBox
from .finance_service import FinanceService


# 声明用户序列化
class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return BaseInfo.objects.create(**validated_data)

    class Meta:
        model = BaseInfo
        # 序列化验证检查，是否要必填的字典
        fields = ['id', 'platform_uid', 'full_name', 'platform_id']


# 声明资金序列化
class FinanceTransactSerializer(serializers.ModelSerializer):
    # 自定义回调函数字段
    lend = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()
    outgo = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    sand_box = serializers.SerializerMethodField()
    transact_time = serializers.SerializerMethodField()
    transact_timestamp = serializers.SerializerMethodField()

    # 自定义外键字段
    # platform = serializers.ReadOnlyField(source='platform.platform_name')
    account_name = serializers.ReadOnlyField(source='account.full_name')
    their_account_name = serializers.ReadOnlyField(source='their_account.full_name')
    pay_mode = serializers.ReadOnlyField(source='pay_mode.pay_mode')
    currency = serializers.ReadOnlyField(source='currency.currency')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Transact.objects.create(**validated_data)

    # 在数据库是否插入内容的字段
    class Meta:
        model = Transact
        fields = [
            'id',
            'transact_id',
            'transact_time',
            'transact_timestamp',
            'account_id',
            'account_name',
            'their_account_id',
            'their_account_name',
            'platform_id',
            'order_no',
            'opposite_account',
            'summary',
            'currency',
            'amount',
            'lend',
            'income',
            'outgo',
            'balance',
            'pay_mode',
            'remark',
            'images',
            'sand_box',
            'goods_info',
            'pay_info',
        ]

    def get_lend(self, obj):
        income = obj.income if obj.income is not None else Decimal(0)
        outgo = obj.outgo if obj.outgo is not None else Decimal(0)
        amount = income - outgo
        return '借' if amount < 0 else '贷' if amount > 0 else '平'

    # 这里是调用了platform这个字段拼成了get_platform
    def get_amount(self, obj):
        income = obj.income if obj.income is not None else Decimal(0)
        outgo = obj.outgo if obj.outgo is not None else Decimal(0)
        return income - outgo

    def get_income(self, obj):
        return obj.income

    def get_outgo(self, obj):
        return obj.outgo

    def get_balance(self, obj):
        return obj.balance

    def get_sand_box(self, obj):
        return obj.sand_box.sand_box_name if obj.sand_box else None

    def get_transact_time(self, obj):
        return obj.transact_time.astimezone(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

    def get_transact_timestamp(self, obj):
        return int(obj.transact_time.timestamp())


class FinanceTransactService:
    @staticmethod
    def get(params, user_id):
        # self.params = request.query_params  # 返回QueryDict类型

        # token = self.request.META.get('HTTP_AUTHORIZATION', '')
        # if not token:
        #     return Response({'err': 4001, 'msg': '缺少Token', })

        # user_id = UserService.check_token(token)
        # if not user_id:
        #     return Response({'err': 4002, 'msg': 'token验证失败', })

        id = params.get('transact_id', None) or params.get('id', None)
        if not id:
            # return Response({'err': 6001, 'msg': '缺少id', })
            return None, '缺少id'

        transact = Transact.objects.filter(id=id).first()
        # print(">>> transact:", transact)
        if not transact:
            return None, '记录不存在'

        serializer = FinanceTransactSerializer(transact, many=False)
        # print(">>> serializer:", serializer)

        # # 翻译
        # output = _("Welcome to my site.")

        return serializer.data, None

        # POST方法，如果无transact_id则是新增，否则为修改

    @staticmethod
    def finance_transact_detailed(transact_id):
        transact = Transact.objects.filter(transact_id=transact_id).first()
        if not transact:
            return None, "不存在"
        return transact, None

    @staticmethod
    def post(param):
        # param = self.params = request.query_params  # 返回QueryDict类型
        item = serializer_params = {}  # 将要写入的某条数据
        # print(param)
        # print(">>> self.params:", self.params)

        # ========== 一、验证权限 ==========

        # token = self.request.META.get('HTTP_AUTHORIZATION', '')
        # if not token:
        #     return Response({'err': 4001, 'msg': '缺少Token', })
        # user_id = UserService.check_token(token)
        # if not user_id:
        #     return Response({'err': 4002, 'msg': 'token验证失败', })

        # ========== 二、必填性检查 ==========

        # if not self.params.get('account_id', ''):
        #     return Response({'err': 1000, 'msg': '缺少account_id', })
        # if not param.get('their_account_id', ''):
        #     return Response({'err': 3301, 'msg': '缺少their_account_id', })
        if not param.get('platform', ''):
            # return Response({'err': 3302, 'msg': '缺少platform', })
            return None, '缺少platform'
        if not param.get('amount', ''):
            # return Response({'err': 3303, 'msg': '缺少amount', })
            return None, '缺少amount'
        if not param.get('currency', ''):
            # return Response({'err': 3304, 'msg': '缺少currency', })
            return None, '缺少currency'
        if not param.get('pay_mode', ''):
            # return Response({'err': 3305, 'msg': '缺少pay_mode', })
            return None, '缺少pay_mode'
        if not param.get('summary', ''):
            # return Response({'err': 3306, 'msg': '缺少summary', })
            return None, '缺少summary'

        # ========== 三、内容的类型准确性检查 ==========
        # 判断无transact_id为新建，否则为修改
        is_create = True
        transact_has_id = Transact.objects.filter(transact_id=param.get('transact_id', ''))
        if transact_has_id:
            is_create = False
        # is_create = 'transact_id' not in param or param['transact_id'] is ''
        # 检查是否有该id
        if not is_create and param.get('id', ''):
            has_id = Transact.objects.filter(id=param.get('id', '')).count() > 0
            if not has_id:
                # return Response({'err': 1001, 'msg': 'id不存在', })
                return None, 'id不存在'
        # 判断平台是否存在
        platform_name = param.get('platform', '')
        # item['platform'] = Platform.objects.filter(platform_name=platform_name).first().platform_id
        # item['platform'] = Platform.objects.filter(platform_name=platform_name).first()
        platform_info, err = UserPlatformService.get_platform_info(platform_name=platform_name)
        # print("> platform_name:", platform_name, platform_info)
        if err:
            # return Response({'err': 1002, 'msg': '平台不存在: ' + platform_name, })
            return None, '平台不存在: ' + platform_name
        item['platform_id'] = platform_info.get('platform_id')
        # 发起交易的账号ID，如果没有则默认自己
        # account_id = int(param.get('account_id', '') or user_id)
        account_id = int(param.get('account_id', ''))
        item['account'] = BaseInfo.objects.filter(id=account_id).first()
        # print("> account:", account_id, item['account'], )
        if not item['account']:
            # return Response({'err': 1003, 'msg': '用户account_id不存在', })
            return None, '用户account_id不存在'
        # 承受交易的账号，要从数据库判断是否存在
        their_account_id = param.get('their_account_id', '')
        # print("> their_account_id:", their_account_id, )
        # 如果有id需要判断是否为数字
        # if their_account_id and not their_account_id.isdecimal():
        #     # return Response({'err': 1004, 'msg': '用户their_account_id必须是数字', })
        #     return None, '用户their_account_id必须是数字'
        if their_account_id:
            their_account_id = int(their_account_id)
        if their_account_id:
            item['their_account'] = BaseInfo.objects.filter(id=their_account_id).first()
            # print("> their_account_id:", their_account_id, item['their_account'])
            if not item['their_account']:
                # return Response({'err': 1004, 'msg': '用户their_account_id不存在', })
                return None, '用户their_account_id不存在'
        # 边界检查，自己不能和自己交易
        if account_id == their_account_id:
            # return Response({'err': 1005, 'msg': '自己不能和自己交易', })
            return None, '自己不能和自己交易'

        # 生成发起交易的用户名 todo 要不用金额会不会更安全？怎么处理重复的可能性
        username = item['account'].user_name
        # print(">>> username:", username)
        # 生成唯一且不可重复的交易ID，且具有校验作用
        # transact_id = param['transact_id'] if not is_create else FinanceService.make_unicode(username)
        if is_create and param.get('transact_id', ''):

            transact_id = param.get('transact_id', '')
        elif is_create and not param.get('transact_id', ''):
            transact_id = FinanceService.make_unicode(username)
        else:
            transact_id = param.get('transact_id', '')

        item['transact_id'] = transact_id

        # print(">>> transact_id:", transact_id)
        if is_create and Transact.objects.filter(transact_id=transact_id).values().count():
            # return Response({'err': 1007, 'msg': '新增时发现复重交易ID，请检查是否有重复记录: ' + transact_id, })
            return None, '新增时发现复重交易ID，请检查是否有重复记录: ' + transact_id
        if not is_create and Transact.objects.filter(transact_id=transact_id).values().count() == 0:
            # return Response({'err': 1008, 'msg': '修改信息的交易ID不存在: ' + transact_id, })
            return None, '修改信息的交易ID不存在: ' + transact_id

        tz = pytz.timezone('Asia/Shanghai')
        # 返回datetime格式的时间
        now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        # 如果没有时间则生成交易时间
        # transact_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        transact_time = param.get('transact_time', '')
        # print(">>> transact_time:", transact_time, )
        # if transact_time else timezone.localtime() if is_create TODO USE_TZ = False 时会报错 如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。
        item['transact_time'] = datetime.strptime(transact_time, '%Y-%m-%d %H:%M:%S') \
            if transact_time else now if is_create \
            else Transact.objects.filter(transact_id=transact_id).first().transact_time
        # print(">>> transact_time:", transact_time, item['transact_time'], type(item['transact_time']))
        if not item['transact_time']:
            # return Response({'err': 1006, 'msg': '交易时间格式不正确', })
            return None, '交易时间格式不正确'

        # 边界检查：币种是否存在
        currency = param.get('currency', '')
        item['currency_set'] = Currency.objects.filter(currency=currency).first()
        # print(">>> currency:", currency, item['currency_set'], type(item['currency_set']))
        if item['currency_set'] is None:
            # return Response({'err': 1009, 'msg': 'currency不存在', })
            return None, 'currency不存在'
        item['currency'] = item['currency_set'].id

        # 判断支付方式，并根据支付方式判断是否要从内部余额中扣款
        pay_mode = param.get('pay_mode', 'BALANCE')
        # 边界检查：支付方式是否存在
        item['pay_mode_set'] = PayMode.objects.filter(pay_mode=pay_mode).first()
        # print(">>> pay_mode:", pay_mode, item['pay_mode_set'])
        if item['pay_mode_set'] is None:
            # return Response({'err': 1010, 'msg': 'pay_mode不存在', })
            return None, 'pay_mode不存在'
        item['pay_mode'] = item['pay_mode_set'].id

        # 支出或收入 ----------------------------------------------------------------------
        if not Jt.is_number(param.get('amount', '')):
            # return Response({'err': 1012, 'msg': 'amount必须是数字', })
            return None, 'amount必须是数字'
        amount = Decimal(param.get('amount', 0.0))  # todo 财务系统不存在四舍五入，一分都不多给
        if amount == 0:
            # return Response({'err': 1013, 'msg': '交易金额不能为0', })
            return None, '交易金额不能为0'
        income = amount if amount > 0 else Decimal(0.0)
        item['income'] = income
        outgo = Decimal(math.fabs(amount)) if amount < 0 else Decimal(0.0)
        item['outgo'] = outgo
        # print(">>> amount:", amount)
        # print(">>> income:", income)
        # print(">>> outgo:", outgo)

        # 沙盒 ----------------------------------------------------------------------
        sand_box_name = param.get('sand_box', '')
        if sand_box_name:
            item['sand_box_set'] = SandBox.objects.filter(sand_box_name=sand_box_name).first()
            # print(">>> sand_box:", sand_box_name, item['sand_box_set'])
            if item['sand_box_set'] is None:
                # return Response({'err': 1011, 'msg': 'sand_box不存在', })
                return None, 'sand_box不存在'
            item['sand_box'] = item['sand_box_set'].id
        # print(">>> sand_box_name: ", sand_box_name)
        # print(">>> item['sand_box']: ", item['sand_box'])

        # 查余额 ---------------------------------------------------------------------
        balance_set = Transact.objects.filter(
            Q(account_id=account_id) &
            Q(currency_id=item['currency']) &
            Q(platform_id=item['platform_id']) &
            Q(transact_time__lt=item['transact_time']) &
            ~Q(transact_id=item['transact_id'])
        )
        # 如果有沙盒。
        if sand_box_name:
            balance_set = balance_set.filter(Q(sand_box_id=item['sand_box']))
        else:
            balance_set = balance_set.filter(Q(sand_box_id=None))

        balance_set = balance_set.order_by('-transact_time').values().first()
        print(">>> balance_set:", balance_set)
        # print(">>> balance_set['balance'] ", balance_set['balance'])
        last_balance = balance_set['balance'] if balance_set is not None else Decimal(0.0)
        # print(">>> last_balance:", last_balance)

        # getcontext().rounding = "ROUND_HALF_UP"  # 真正四舍五入
        # getcontext().prec = 2  # //保留两位小数 打开这个后有时候会变成整数，为什么？
        # 如果是余额支付则内部交易，否则是第三方支付，如微信、支付宝等
        # is_inside_pay = True if pay_mode.upper() == 'BALANCE' else False
        # print(">>> is_inside_pay:", is_inside_pay)
        # balance = last_balance + income - (outgo if is_inside_pay else Decimal(0.0))

        item['balance'] = last_balance
        if pay_mode == "BALANCE":
            balance = last_balance + income - outgo
            # print(">>> balance:", balance)
            item['balance'] = balance
        # if balance < 0:
        #     return Response({'err': 1014, 'msg': '余额不足，待扣金额为'+str(amount)+'，当前余额为'+str(last_balance)+',差额'+str(balance) })

        # 平台订单号是可以允许重复的，如果没有平台订单号则输入交易号
        order_no = int(param.get('order_no', transact_id))  # 如果没有平台订单号则填交易号
        item['order_no'] = order_no

        # 对方科目
        opposite_account = param.get('opposite_account', '')
        item['opposite_account'] = opposite_account

        # 摘要
        summary = param.get('summary', '')
        item['summary'] = summary

        # 商品信息
        goods_info = param.get('goods_info', '')
        item['goods_info'] = goods_info

        # 支付信息
        pay_info = param.get('pay_info', '')
        item['pay_info'] = pay_info

        # 备注
        remark = param.get('remark', '')
        item['remark'] = remark

        # 上传图片
        images = param.get('images', '')
        item['images'] = images

        # ========== 四、相关前置业务逻辑处理 ==========

        # 在新建订单时：如果平台订单号重复，金额不能重复，收方和支出方不能重复，金额也不能重复。
        if is_create:
            repeat_order_set = Transact.objects.filter(
                Q(order_no=order_no) &
                Q(account_id=account_id) &
                (Q(income=income) | Q(outgo=outgo))
            )
            # 单独判断，当有对方账号ID时才判断，因为在设计上对方账号是可以自动生成的
            if their_account_id:
                repeat_order_set.filter(Q(their_account_id=their_account_id))
            if repeat_order_set.count() > 0:
                # return Response({'err': 1015, 'msg': '重复的交易订单号：' + str(order_no), })
                return None, '重复的交易订单号：' + str(order_no)
        # --------------------------------------------------------------------------------------

        if not param.get('their_account_id', '') and not param.get('their_account_name', ''):
            # return Response({'err': 1016, 'msg': 'their_account_id或their_account_name 必填', })
            return None, 'their_account_id或their_account_name 必填'
        # 没有对方账户ID时从对方账户名创建一个账户
        # 如果无their_account_id、有their_account_name，则用their_account_name生成一个their_account_id
        # TODO 貌似该功能不能使用 作废
        if not param.get('their_account_id', '') and param.get('their_account_name', ''):
            their_account_name = param['their_account_name']
            #     platform_id = BaseInfo.objects.get(id=account_id).platform_id
            new_user_param = {
                # "platform_id": platform_id,
                "full_name": their_account_name,
                # "platform_uid": str(int(time.time())) + FinanceTransactService.random_four_int(),  # 这样写好吗？
            }
            new_user = BaseInfo.objects.create(**new_user_param)
            #     # 增加一个用户
            #     user_serializer = UserSerializer(data=new_user_param, context={})
            #     # print(">>> user_serializer ", user_serializer)
            #     if not user_serializer.is_valid():
            #         # return Response({'err': 1017, 'msg': user_serializer.errors, })
            #         return None, user_serializer.errors
            #     user_serializer.validated_data['platform_id'] = platform_id
            #     # print(">>> user_serializer.validated_data['platform_id']", user_serializer.validated_data['platform_id'])
            #     user_serializer.save()
            #     # 这是什么写法？传递引用了两次呢
            #     item['their_account_id'] = BaseInfo.objects.get(platform_uid=new_user_param['platform_uid']).id
            item['their_account_id'] = new_user.id
            item['their_account'] = BaseInfo.objects.get(id=item['their_account_id'])
        # -------------------------------------------------------------------------------------

        # 如果有id，则是修改数据
        if is_create:
            response = FinanceTransactService.create(item)
        else:
            response = FinanceTransactService.update(item)

        return response

    # 增
    @staticmethod
    def create(item):
        # print(">>> create:", item, )
        # 增加一个交易记录
        serializer = FinanceTransactSerializer(data=item, context={})

        # 验证失败，获取错误信息
        if not serializer.is_valid():
            # print(">>> serializer.errors:", serializer.errors, "\n")
            # 调用save(), 从而调用序列化对象的create()方法,创建一条数据
            # return Response({'err': 1018, 'msg': serializer.errors, })
            return None, serializer.errors

        # 验证成功，获取数据
        serializer.validated_data['platform_id'] = item['platform_id']
        serializer.validated_data['account'] = item['account']
        serializer.validated_data['their_account'] = item['their_account']
        serializer.validated_data['pay_mode'] = item['pay_mode_set']
        serializer.validated_data['currency'] = item['currency_set']
        serializer.validated_data['sand_box'] = item.get('sand_box_set', None)
        serializer.validated_data['income'] = item['income']
        serializer.validated_data['outgo'] = item['outgo']
        serializer.validated_data['balance'] = item['balance']
        serializer.validated_data['transact_time'] = item['transact_time']

        # print(">>> serializer.validated_data: ", serializer.validated_data,)
        # print(">>> serializer: ", serializer,)

        serializer.save()

        FinanceService.check_balance(account_id=item['account'].id,
                                     platform_id=item['platform_id'],
                                     currency=item['currency_set'].currency,
                                     sand_box=item.get('sand_box_set', None))

        # return Response({
        #     'err': 0,
        #     'msg': '新增成功',
        # })
        return None, None

    # 改
    @staticmethod
    def update(item):
        # print(">>> update:", item, )

        transact = Transact.objects.filter(transact_id=item['transact_id']).first()
        update_serializer = FinanceTransactSerializer(data=item, instance=transact)
        if not update_serializer.is_valid():
            # print(">>> serializer.errors:", serializer.errors, "\n")
            # 调用save(), 从而调用序列化对象的create()方法,创建一条数据
            # return Response({'err': 1019, 'msg': update_serializer.errors, })
            return None, update_serializer.errors
        # 验证成功，获取数据
        update_serializer.validated_data['platform_id'] = item['platform_id']
        update_serializer.validated_data['account'] = item['account']
        update_serializer.validated_data['their_account'] = item['their_account']
        update_serializer.validated_data['pay_mode'] = item['pay_mode_set']
        update_serializer.validated_data['currency'] = item['currency_set']
        update_serializer.validated_data['sand_box'] = item.get('sand_box_set', None)
        update_serializer.validated_data['income'] = item['income']
        update_serializer.validated_data['outgo'] = item['outgo']
        update_serializer.validated_data['balance'] = item['balance']
        update_serializer.validated_data['transact_time'] = item['transact_time']

        update_serializer.save()

        FinanceService.check_balance(account_id=item['account'].id,
                                     platform_id=item['platform_id'],
                                     currency=item['currency_set'].currency,
                                     sand_box=item.get('sand_box_set', None))

        # return Response({
        #     'err': 0,
        #     'msg': '更新成功',
        # })
        return None, None

    # 生成随机的4位数数字
    @staticmethod
    def random_four_int():
        str = ""
        for i in range(4):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        return str
