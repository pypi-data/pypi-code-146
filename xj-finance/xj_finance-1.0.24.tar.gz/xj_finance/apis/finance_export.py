# _*_coding:utf-8_*_
# 引入系统库
import os
from django.db.models import Q
# 引入序列化库
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# 引入excel库

# 引入本地文件
from xj_user.services.user_service import UserService
from utils.utils import Jt
from xj_finance.models import *
from xj_finance.services import FinanceService

print("-" * 30, os.path.basename(__file__), "-" * 30)


# 声明序列化
class ExportExcelSerializer(ModelSerializer):
    class Meta:
        model = Transact
        # 序列化验证检查，检查必填项的字段
        fields = '__all__'


# 视图方法可以返回REST framework的Response对象,视图会为响应数据设置（render）符合前端要求的格式
class ExportExcel(APIView):
    params = None
    serializer_params = None

    use_model = Transact
    queryset = use_model.objects.all()
    serializer_class = ExportExcelSerializer

    def post(self, request, *args, **kwargs):
        # try:
        # 使用Postman Body form-data 输入参数
        param = self.params = request.data
        # print(">>> param:", param)

        # ========== 一、检查：验证权限 ==========
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return Response({'err': 6001, 'msg': '缺少Token', })
        user_id = UserService.check_token(token)
        if not user_id:
            return Response({'err': 6002, 'msg': 'token验证失败', })

        # ========== 二、检查：必填性 ==========
        if not param.get('format', ''):
            return Response({'err': 2001, 'msg': '缺少format', })
        if param['format'] not in ['xlsx', 'xls', 'csv']:
            return Response({'err': 2002, 'msg': '导出格式错误，可填 xlsx 或 xls 或 csv', })

        format = param['format']

        id_list = param.get('data')
        # 过滤
        obj_list = self.queryset.filter(Q(account=user_id))
        # print(">>> id_list:", id_list)
        # print(">>> obj_list:", obj_list)

        # 如果id_list有值，表示导出部分，否则导出全部
        if id_list:
            obj_list = obj_list.filter(Q(id__in=id_list))

        # 过滤平台
        platform_name = param.get('platform', '')
        if platform_name:
            FinanceService.transact_filter(param_name=platform_name, obj_list=obj_list)

        # 筛选币种
        currency = param.get('currency', '')
        if currency:
            FinanceService.transact_filter(param_name=currency, obj_list=obj_list)

        # 筛选支付方式
        pay_mode = param.get('pay_mode', '')
        if pay_mode:
            FinanceService.transact_filter(param_name=pay_mode, obj_list=obj_list)

        # 筛选沙盒
        sand_box = param.get('sand_box', '')
        sand_box = sand_box if sand_box else None
        if sand_box:
            FinanceService.transact_filter(param_name=sand_box, obj_list=obj_list)

        # 模糊筛选对方账号
        their_account_name = param.get('their_account_name', '')
        if their_account_name:
            FinanceService.transact_filter(param_name=their_account_name, obj_list=obj_list)

        # 筛选摘要，模糊搜索
        search_word = param.get('search_word', '')
        if search_word:
            FinanceService.transact_filter(param_name=search_word, obj_list=obj_list)

        ser = ExportExcelSerializer(instance=obj_list, many=True)
        # print(">>> ser: ", ser)
        # print(">>> ser.data: ", ser.data)  # [OrderedDict([(),],[OrderedDict([(),]

        meta_fields = Transact._meta.fields
        name_list = [field.name for field in meta_fields]
        header_list = [field.verbose_name for field in meta_fields]

        file_name = 'FinanceTransact' + '_' + Jt.make_datetime_17()

        obj_list = ser.data
        # print(">>> obj_list ", obj_list)
        data_list = []
        for obj in obj_list:
            data = [obj[name] for name in name_list]
            data_list.append(data)
        # print(">>> data_list", data_list)

        Jt.write_data_to_excel(save_dir='excel/', filename=file_name,
                               format=format, header_list=header_list,
                               data_list=data_list)

        return Response({
            'err': 0,
            'msg': '导出数据成功!',
            'data': '',
        })

        # except:
        #     return Response({
        #         'err': 1,
        #         'msg': '导出数据出错!',
        #         'data': '',
        #     })


