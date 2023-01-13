from decimal import Decimal
import random

import pytz
from django.db.models import Q
from django.forms import model_to_dict
from rest_framework import serializers
from pathlib import Path
from main.settings import BASE_DIR
from xj_enroll.utils.custom_tool import format_params_handle
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_user.models import BaseInfo
from .finance_service import FinanceService
from ..models import Transact
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))

sand_box_meet = main_config_dict.sand_box_meet or module_config_dict.sand_box_meet or ""
sand_box_receivable = main_config_dict.sand_box_receivable or module_config_dict.sand_box_receivable or ""


# 声明用户序列化
class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return BaseInfo.objects.create(**validated_data)

    class Meta:
        model = BaseInfo
        # 序列化验证检查，是否要必填的字典
        fields = ['id', 'platform_uid', 'full_name', 'platform_id']


class FinanceTransactsSerializer(serializers.ModelSerializer):
    # 方法一：使用SerializerMethodField，并写出get_platform, 让其返回你要显示的对象就行了
    # p.s.SerializerMethodField在model字段显示中很有用。
    # order = serializers.SerializerMethodField()
    lend = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    transact_time = serializers.SerializerMethodField()
    # transact_timestamp = serializers.SerializerMethodField()
    sand_box = serializers.SerializerMethodField()
    distinguish = serializers.SerializerMethodField()

    # # 方法二：增加一个序列化的字段platform_name用来专门显示品牌的name。当前前端的表格columns里对应的’platform’列要改成’platform_name’
    # account_id = serializers.ReadOnlyField(source='account.id')
    account_name = serializers.ReadOnlyField(source='account.full_name')
    # their_account_id = serializers.ReadOnlyField(source='their_account.id')
    their_account_name = serializers.ReadOnlyField(source='their_account.full_name')
    # platform_id = serializers.ReadOnlyField(source='platform.platform_id')
    # platform_name = serializers.ReadOnlyField(source='platform.platform_name')
    # platform = serializers.ReadOnlyField(source='platform.platform_name')
    pay_mode = serializers.ReadOnlyField(source='pay_mode.pay_mode')
    currency = serializers.ReadOnlyField(source='currency.currency')

    # income = serializers.ReadOnlyField(source='income')
    # outgo = serializers.ReadOnlyField(source='outgo')

    class Meta:
        model = Transact
        fields = [
            # 'order',
            'id',
            # 'transact_no',
            'transact_no',
            'transact_time',
            # 'transact_timestamp',
            'platform_id',
            # 'platform_name',
            # 'platform',
            # 'account_id',
            'account_name',
            # 'their_account_id',
            'their_account_name',
            'order_no',
            'opposite_account',
            'summary',
            'currency',
            # 'income',
            # 'outgo',
            'lend',
            'amount',
            'balance',
            'pay_mode',
            # 'goods_info',
            # 'pay_info',
            'sand_box',
            'remark',
            'images',
            'is_reverse',
            'is_delete',
            'is_write_off',
            'distinguish'
        ]

    # def get_order(self, obj):
    #     print("get_order:", obj.id, obj, self)
    #     return 1

    def get_lend(self, obj):
        income = obj.income if obj.income is not None else Decimal(0)
        outgo = obj.outgo if obj.outgo is not None else Decimal(0)
        amount = income - outgo
        return '借' if amount < 0 else '贷' if amount > 0 else '平'

    def get_amount(self, obj):
        income = obj.income if obj.income is not None else Decimal(0)
        outgo = obj.outgo if obj.outgo is not None else Decimal(0)
        return income - outgo

    def get_balance(self, obj):
        balance = obj.balance
        return balance

    def get_sand_box(self, obj):
        return obj.sand_box.sand_box_name if obj.sand_box else None

    def get_transact_time(self, obj):
        return obj.transact_time.astimezone(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

    # def get_transact_timestamp(self, obj):
    #     return int(obj.transact_time.timestamp())


class FinanceTransactsService:
    @staticmethod
    def get(params, user_id):
        # ========== 三、内容的类型准确性检查 ==========

        valid = FinanceService.check_filter_validity(params=params)
        print(">>> check_filter_validity", valid)
        if valid['err'] > 0:
            # return Response({'err': valid['err'], 'msg': valid['msg'], })
            return None, valid['msg']
        transacts = Transact.objects.filter(account_id=user_id).filter(**valid['query_dict'])
        transacts = transacts.order_by('-transact_time')

        print(">>> transacts: ", transacts)

        # statistic_list = []
        # aggr = transacts.aggregate(
        #     outgo=Sum('outgo', filter=Q(currency__currency='CNY')),
        #     income=Sum('income', filter=Q(currency__currency='CNY')),
        # )
        # aggr['income'] = aggr['income'] or Decimal(0.0)
        # aggr['outgo'] = aggr['outgo'] or Decimal(0.0)
        # aggr['balance'] = aggr['income'] - aggr['outgo']
        # statistic_list.append(aggr)

        # images = 'http://' + request.headers['Host'] + ''

        # ========== 四、相关前置业务逻辑处理 ==========

        # ========== 五、翻页 ==========

        page = int(params['page']) - 1 if 'page' in params else 0
        size = int(params['size']) if 'size' in params else 10

        total = transacts.count()

        current_page_set = transacts[page * size: page * size + size] if page >= 0 and size > 0 else transacts

        serializer = FinanceTransactsSerializer(current_page_set, many=True)

        res_list = []
        for i, it in enumerate(serializer.data):
            # print("current_page_set:", i, it)
            it['order'] = page * size + i + 1
            it['platform_name'] = params.get('platform', '')
            res_list.append(it)

        # return {'total': total, 'list': res_list, 'statistics': statistic_list}, None

        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': res_list}, None

        # return {'total': total, 'list': res_list}, None
        # 翻译
        # output = _("Welcome to my site.")

        # return Response({
        #     'err': 0,
        #     'msg': 'OK',
        #     'data': {'total': total, 'list': res_list, 'statistics': statistic_list},
        #     # 'data': output,
        # })

    # 生成随机的4位数数字
    @staticmethod
    def random_four_int():
        str = ""
        for i in range(4):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        return str

    @staticmethod
    def detail(pk=None, order_no=None, transact_no=None, field_list=None):
        """
        查询订单性情
        """
        if not pk and not order_no and not transact_no:
            return None, None

        transact_obj = Transact.objects

        if pk:
            transact_filter_obj = transact_obj.filter(id=pk).first()
        elif order_no:
            transact_filter_obj = transact_obj.filter(order_no=order_no).first()
        elif transact_no:
            transact_filter_obj = transact_obj.filter(transact_no=transact_no).first()
        else:
            return None, "没有找到对应的数据"

        if not transact_filter_obj:
            return None, "没有找到对应的数据"

        transact_dict = transact_filter_obj.to_json()

        transact_filter_dict = format_params_handle(
            param_dict=transact_dict,
            filter_filed_list=field_list
        )
        return transact_filter_dict, None

    @staticmethod
    def detail_all(order_no=None):
        """
        查询订单性情
        """
        if not order_no:
            return None, None

        transact_obj = Transact.objects

        if order_no:
            transact_filter_obj = transact_obj.filter(
                order_no=order_no, sand_box__isnull=False).values("order_no", "transact_no",
                                                                  "account_id",
                                                                  "enroll_id",
                                                                  "their_account_id",
                                                                  "platform_id",
                                                                  "income", "outgo", "balance",
                                                                  "currency_id", "pay_mode_id",
                                                                  "summary", "distinguish")
        else:
            return None, "没有找到对应的数据"

        if not transact_filter_obj:
            return None, "没有找到对应的数据"

        # print(model_to_list(transact_filter_obj))
        return transact_filter_obj, None

    @staticmethod
    def distribution(params):
        order_no = params.get("order_no", "")
        # payment_category = params.get("payment_category  ", "meet")  # 款项类目 receivable 应收 meet 应付
        amount = params.get('amount', 0.0)  # 如果是负数是应付反之是应收
        two_level = params.get('two_level', "")  # 是否为二级分销
        receivable_data = {}  # 应收数据
        meet_data = {}  # 应付数据
        # 查询交易信息
        finance_transact_data, err = FinanceTransactsService.detail(order_no=order_no)
        if err:
            return None, err
        else:
            if two_level == 'True':
                two_level = True
            elif two_level == 'False':
                two_level = False
            # 获取交易流水号
            transact_no = finance_transact_data['transact_no'].rstrip(finance_transact_data['transact_no'][-1])
            # 获取报名id
            enroll_id = finance_transact_data['enroll_id']
            # 应付数据
            receivable_data['sand_box'] = sand_box_meet  # 沙盒应付
            receivable_data['transact_no'] = transact_no + '4'  # 流水号
            receivable_data['amount'] = -abs(float(amount))
            receivable_data['account_id'] = finance_transact_data['their_account_id']
            receivable_data['their_account_id'] = None
            receivable_data['order_no'] = order_no  # 订单号
            receivable_data['currency_id'] = finance_transact_data['currency_id']  # 币种
            receivable_data['pay_mode_id'] = finance_transact_data['pay_mode_id']  # 支付方式
            receivable_data['platform_id'] = finance_transact_data['platform_id']  # 所属平台
            receivable_data['summary'] = finance_transact_data['summary']  # 摘要说明
            receivable_data['distinguish'] = "PAYABLE"  # 交易区分标识
            # 应收数据
            meet_data['sand_box'] = sand_box_receivable  # 沙盒应收
            meet_data['transact_no'] = transact_no + '3'  # 流水号
            meet_data['amount'] = amount
            meet_data['account_id'] = None  # 报名人id
            meet_data['their_account_id'] = finance_transact_data['their_account_id']
            meet_data['order_no'] = order_no  # 订单号
            meet_data['currency_id'] = finance_transact_data['currency_id']  # 币种
            meet_data['pay_mode_id'] = finance_transact_data['pay_mode_id']  # 支付方式
            meet_data['platform_id'] = finance_transact_data['platform_id']  # 所属平台
            meet_data['summary'] = finance_transact_data['summary']  # 摘要说明
            meet_data['distinguish'] = "RECEIVABLE"  # 交易区分标识

            while True:
                number = ''.join(str(x) for x in random.sample(range(10), 3))
                number1 = ''.join(str(x) for x in random.sample(range(10), 3))
                if not number.startswith('0') and not number1.startswith('0'):
                    break

            if two_level:
                # 生成不重复的 订单流水号
                while True:
                    receivable_data['transact_no'] = transact_no.rstrip(receivable_data['transact_no'][-1]) + str(
                        int(receivable_data['transact_no'][-1]) + int(number))
                    meet_data['transact_no'] = transact_no.rstrip(meet_data['transact_no'][-1]) + str(
                        int(meet_data['transact_no'][-1]) + int(number1))

                    receivable = Transact.objects.filter(transact_no=receivable_data['transact_no']).exists()
                    meet = Transact.objects.filter(transact_no=meet_data['transact_no']).exists()
                    if not receivable and not meet:
                        break

            print("应付", receivable_data)
            receivable_finance_transact, receivable_err = FinanceTransactService.post(receivable_data)
            if receivable_err:
                return None, receivable_err
            print("应收", meet_data)
            meet_finance_transact, meet_err = FinanceTransactService.post(meet_data)
            if meet_err:
                return None, meet_err
            return None, None

    @staticmethod
    def write_off(params):
        order_no = params.get("order_no", "")
        type = params.get("type", "")
        finance_transact_data, err = FinanceTransactsService.detail_all(order_no=order_no)
        if err:
            return None, err
        for v in finance_transact_data:
            transact_no = v['transact_no']
            if type == "write_off":
                v['transact_no'] = transact_no.rstrip(transact_no[-1]) + str(int(transact_no[-1])) + "-2"
                finance_transact, post_err = FinanceTransactService.post(v)
                if post_err:
                    return None, post_err
                # 生成真实记录成功后 原沙盒记录改为核销
                Transact.objects.filter(transact_no=transact_no).update(is_write_off=1, is_reverse=None)  # 沙盒核销
            elif type == "reverse":
                Transact.objects.filter(transact_no=transact_no).update(is_reverse=1, is_write_off=None)  # 沙盒红冲
        return None, None
