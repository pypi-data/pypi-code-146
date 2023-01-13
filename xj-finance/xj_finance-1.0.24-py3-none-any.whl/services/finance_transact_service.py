from decimal import Decimal
import math
import random

from django.db.models import Q
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.datetime_safe import datetime
import pytz
from rest_framework import serializers

from xj_user.models import BaseInfo
from xj_user.services.user_platform_service import UserPlatformService
from .finance_service import FinanceService
from ..models import Transact, Currency, PayMode, SandBox
from ..utils.jt import Jt


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
    distinguish = serializers.SerializerMethodField()

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
            'transact_no',
            'transact_time',
            'transact_timestamp',
            'account_id',
            'account_name',
            'their_account_id',
            'their_account_name',
            'platform_id',
            'enroll_id',
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
            'distinguish'
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

        id = params.get('transact_no', None) or params.get('id', None)
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

        # POST方法，如果无transact_no则是新增，否则为修改

    @staticmethod
    def finance_transact_detailed(transact_no):
        transact = Transact.objects.filter(transact_no=transact_no).first()
        if not transact:
            return None, "不存在"
        return transact, None

    @staticmethod
    def post(param):
        item = serializer_params = {}  # 将要写入的某条数据

        # ========== 一、验证权限 ==========

        # token = self.request.META.get('HTTP_AUTHORIZATION', '')
        # if not token:
        #     return Response({'err': 4001, 'msg': '缺少Token', })
        # user_id = UserService.check_token(token)
        # if not user_id:
        #     return Response({'err': 4002, 'msg': 'token验证失败', })

        # ========== 二、必填性检查 ==========
        if not param.get('platform', '') and not param.get('platform_id', ''):
            return None, '缺少platform'
        if not param.get('amount', '') and not param.get('income', '') and not param.get('outgo', ''):
            return None, '缺少amount'
        if not param.get('currency', '') and not param.get('currency_id', ''):
            return None, '缺少currency'
        if not param.get('pay_mode', '') and not param.get('pay_mode_id', ''):
            return None, '缺少pay_mode'
        if not param.get('summary', ''):
            return None, '缺少summary'
        # ========== 三、内容的类型准确性检查 ==========
        # 判断无transact_no为新建，否则为修改
        is_create = True
        transact_has_id = Transact.objects.filter(transact_no=param.get('transact_no', ''))
        if transact_has_id:
            is_create = False
        # 检查是否有该id
        if not is_create and param.get('id', ''):
            has_id = Transact.objects.filter(id=param.get('id', '')).count() > 0
            if not has_id:
                return None, 'id不存在'
        # 判断平台是否存在
        if not param.get('platform_id', ''):
            platform_name = param.get('platform', '')
            platform_info, err = UserPlatformService.get_platform_info(platform_name=platform_name)
            if err:
                return None, '平台不存在: ' + platform_name
            item['platform_id'] = platform_info.get('platform_id')
        else:
            item['platform_id'] = param.get('platform_id', '')
        # 发起交易的账号ID，如果没有则默认自己
        account_id = int(param.get('account_id', ''))
        item['account'] = BaseInfo.objects.filter(id=account_id).first()
        if not item['account']:
            return None, '用户account_id不存在'
        # 承受交易的账号，要从数据库判断是否存在
        their_account_id = param.get('their_account_id', '')
        if their_account_id:
            their_account_id = int(their_account_id)
        if their_account_id:
            item['their_account'] = BaseInfo.objects.filter(id=their_account_id).first()
            if not item['their_account']:
                return None, '用户their_account_id不存在'
        # 边界检查，自己不能和自己交易
        if account_id == their_account_id:
            return None, '自己不能和自己交易'

        # 生成发起交易的用户名 todo 要不用金额会不会更安全？怎么处理重复的可能性
        username = item['account'].user_name
        # 生成唯一且不可重复的交易ID，且具有校验作用
        if is_create and param.get('transact_no', ''):

            transact_no = param.get('transact_no', '')
        elif is_create and not param.get('transact_no', ''):
            transact_no = FinanceService.make_unicode(username)
        else:
            transact_no = param.get('transact_no', '')

        item['transact_no'] = transact_no
        if is_create and Transact.objects.filter(transact_no=transact_no).values().count():
            return None, '新增时发现复重交易ID，请检查是否有重复记录: ' + transact_no
        if not is_create and Transact.objects.filter(transact_no=transact_no).values().count() == 0:
            return None, '修改信息的交易ID不存在: ' + transact_no
        tz = pytz.timezone('Asia/Shanghai')
        # 返回datetime格式的时间
        now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        # 如果没有时间则生成交易时间
        transact_time = str(param.get('transact_time', ''))
        # if transact_time else timezone.localtime() if is_create TODO USE_TZ = False 时会报错 如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。
        item['transact_time'] = datetime.strptime(transact_time, '%Y-%m-%d %H:%M:%S') \
            if transact_time else now if is_create \
            else Transact.objects.filter(transact_no=transact_no).first().transact_time
        if not item['transact_time']:
            return None, '交易时间格式不正确'

        # 边界检查：币种是否存在
        if not param.get('currency_id', ''):
            currency = param.get('currency', '')
            item['currency_set'] = Currency.objects.filter(currency=currency).first()
            if item['currency_set'] is None:
                return None, 'currency不存在'
            item['currency'] = item['currency_set'].id
        else:
            item['currency_set'] = Currency.objects.filter(id=param.get('currency_id', '')).first()
            if item['currency_set'] is None:
                return None, 'currency不存在'
            item['currency'] = param.get('currency_id', '')

        # 判断支付方式，并根据支付方式判断是否要从内部余额中扣款
        if not param.get('pay_mode_id', ''):
            pay_mode = param.get('pay_mode', '')
            # 边界检查：支付方式是否存在
            item['pay_mode_set'] = PayMode.objects.filter(pay_mode=pay_mode).first()
            if item['pay_mode_set'] is None:
                return None, 'pay_mode不存在'
            item['pay_mode'] = item['pay_mode_set'].id
        else:
            item['pay_mode_set'] = PayMode.objects.filter(id=param.get('pay_mode_id', '')).first()
            if item['pay_mode_set'] is None:
                return None, 'pay_mode不存在'
            item['pay_mode'] = param.get('pay_mode_id', '')

            # 支出或收入 ----------------------------------------------------------------------
        if not param.get('income', '') and not param.get('outgo', ''):
            if not Jt.is_number(param.get('amount', '')):
                return None, 'amount必须是数字'
            amount = Decimal(param.get('amount', 0.0))  # todo 财务系统不存在四舍五入，一分都不多给
            if amount == 0:
                return None, '交易金额不能为0'
            income = amount if amount > 0 else Decimal(0.0)
            item['income'] = income
            outgo = Decimal(math.fabs(amount)) if amount < 0 else Decimal(0.0)
            item['outgo'] = outgo
        else:
            income = param.get('income', '')
            item['income'] = income
            outgo = param.get('outgo', '')
            item['outgo'] = outgo

        enroll_id = param.get('enroll_id', '')
        if enroll_id:
            item['enroll_id'] = enroll_id

        if param.get('distinguish', ''):
            item['distinguish'] = param.get('distinguish', '')

        item['sand_box'] = None
        # 沙盒 ----------------------------------------------------------------------
        sand_box_name = param.get('sand_box', '')
        if sand_box_name:
            item['sand_box_set'] = SandBox.objects.filter(sand_box_name=sand_box_name).first()
            if item['sand_box_set'] is None:
                return None, 'sand_box不存在'
            item['sand_box'] = item['sand_box_set'].id

        # 查余额 ---------------------------------------------------------------------
        balance_set = Transact.objects.filter(
            Q(account_id=account_id) &
            Q(currency_id=item['currency']) &
            Q(platform_id=item['platform_id']) &
            Q(transact_time__lt=item['transact_time']) &
            ~Q(transact_no=item['transact_no'])
        )
        # 如果有沙盒。
        if sand_box_name:
            balance_set = balance_set.filter(Q(sand_box_id=item['sand_box']))
        else:
            balance_set = balance_set.filter(Q(sand_box_id=None))

        balance_set = balance_set.order_by('-transact_time').values().first()
        last_balance = balance_set['balance'] if balance_set is not None else Decimal(0.0)

        item['balance'] = last_balance
        if item['pay_mode_set'].pay_mode == "BALANCE":
            balance = last_balance + income - outgo
            item['balance'] = balance

        # 平台订单号是可以允许重复的，如果没有平台订单号则输入交易号
        order_no = int(param.get('order_no', transact_no))  # 如果没有平台订单号则填交易号
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
                Q(sand_box_id=item['sand_box']) &
                Q(order_no=order_no) &
                Q(account_id=account_id) &
                (Q(income=income) | Q(outgo=outgo))
            )
            # 单独判断，当有对方账号ID时才判断，因为在设计上对方账号是可以自动生成的
            if their_account_id:
                repeat_order_set.filter(Q(their_account_id=their_account_id))
            # if repeat_order_set.count() > 0:
            # return Response({'err': 1015, 'msg': '重复的交易订单号：' + str(order_no), })
            # return None, '重复的交易订单号：' + str(order_no)
        # --------------------------------------------------------------------------------------

        if not param.get('their_account_id', '') and not param.get('their_account_name', ''):
            # return Response({'err': 1016, 'msg': 'their_account_id或their_account_name 必填', })
            return None, 'their_account_id或their_account_name 必填'
        # 没有对方账户ID时从对方账户名创建一个账户
        # 如果无their_account_id、有their_account_name，则用their_account_name生成一个their_account_id
        if not param.get('their_account_id', '') and param.get('their_account_name', ''):
            their_account_name = param['their_account_name']
            base_info = BaseInfo.objects.filter(nickname=their_account_name).first()
            if base_info:
                base_info = model_to_dict(base_info)
                item['their_account_id'] = base_info['id']
                item['their_account'] = BaseInfo.objects.get(id=item['their_account_id'])
            else:
                new_user_param = {
                    "full_name": their_account_name,
                    "nickname": their_account_name,
                }
                new_user = BaseInfo.objects.create(**new_user_param)
                item['their_account_id'] = new_user.id
                item['their_account'] = BaseInfo.objects.get(id=item['their_account_id'])
        # -------------------------------------------------------------------------------------

        # 如果有id，则是修改数据
        if is_create:
            response = FinanceTransactService.create(item)
        else:
            response = FinanceTransactService.update(item)
        # return None
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
        serializer.validated_data['enroll_id'] = item.get('enroll_id', None)
        serializer.validated_data['their_account'] = item['their_account']
        serializer.validated_data['pay_mode'] = item['pay_mode_set']
        serializer.validated_data['currency'] = item['currency_set']
        serializer.validated_data['sand_box'] = item.get('sand_box_set', None)
        serializer.validated_data['income'] = item['income']
        serializer.validated_data['outgo'] = item['outgo']
        serializer.validated_data['balance'] = item['balance']
        serializer.validated_data['transact_time'] = item['transact_time']
        serializer.validated_data['distinguish'] = item.get('distinguish', None)

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

        transact = Transact.objects.filter(transact_no=item['transact_no']).first()
        update_serializer = FinanceTransactSerializer(data=item, instance=transact)
        if not update_serializer.is_valid():
            # print(">>> serializer.errors:", serializer.errors, "\n")
            # 调用save(), 从而调用序列化对象的create()方法,创建一条数据
            # return Response({'err': 1019, 'msg': update_serializer.errors, })
            return None, update_serializer.errors
        # 验证成功，获取数据
        update_serializer.validated_data['platform_id'] = item['platform_id']
        update_serializer.validated_data['account'] = item['account']
        update_serializer.validated_data['enroll_id'] = item.get('enroll_id', None)
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

    @staticmethod
    def get_finance_by_user(user_id):
        user_finance = Transact.objects.filter(account_id=user_id).order_by("-id").values()
        if not user_finance:
            return None, None
        return user_finance.first(), None
