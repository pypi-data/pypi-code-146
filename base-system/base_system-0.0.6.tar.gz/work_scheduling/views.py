from datetime import datetime
import json

import xlrd
import xlrd2
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.template.defaultfilters import title
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
# Create your views here.
from base_system.appointment_ser import HospitalSerializer, OfficeSerializer, DoctorSerializer
from base_system.models import Hospital, Office, Doctor
from base_system.models import Hospital
from base_system.views import column_header, body
# from patient_account.models import AppointmentRecord
from .serializers import *
from rest_framework.response import Response
from copy import copy
import django_filters as filters


class WorkSchedulingMainViewSet(ModelViewSet):
    queryset = WorkSchedulingMain.objects.filter(is_active=True)
    serializer_class = WorkSchedulingMainSerializer
    pagination_class = None
    filter_fields = "__all__"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = copy(request.data)
        ws_schedule_days = data.pop('ws_schedule_days')
        print(ws_schedule_days)
        print(111, request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=True,
                                         context={'ws_schedule_days': ws_schedule_days})
        serializer.is_valid(raise_exception=True)
        # print(222,serializer.data)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class WorkSchedulingMainDoctorViewSet(ModelViewSet):
    queryset = WorkSchedulingMain.objects.filter(is_active=True)
    serializer_class = WorkSchedulingMainDoctorSerializer
    pagination_class = None
    filter_fields = "__all__"


class ScheduleDayViewSet(ModelViewSet):
    queryset = ScheduleDay.objects.filter(is_active=True)
    serializer_class = ScheduleDaySerializer
    pagination_class = None
    filter_fields = "__all__"


class WorkShiftViewSet(ModelViewSet):
    queryset = WorkShift.objects.filter(is_active=True)
    serializer_class = WorkShiftSerializer
    pagination_class = None
    filter_fields = "__all__"


class WorkShiftTypeViewSet(ModelViewSet):
    queryset = WorkShiftType.objects.filter(is_active=True)
    serializer_class = WorkShiftTypeSerializer
    pagination_class = None
    filter_fields = "__all__"


class DoctorWorkSchedulingMainViewSet(ModelViewSet):
    queryset = DoctorWorkSchedulingMain.objects.filter(is_active=True)
    serializer_class = DoctorWorkSchedulingMainSerializer
    pagination_class = None
    filter_fields = "__all__"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = copy(request.data)
        ws_doctor_schedule_days = data.pop('ws_doctor_schedule_days')
        instance = self.get_object()
        print(request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=True,
                                         context={'ws_doctor_schedule_days': ws_doctor_schedule_days})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DoctorScheduleDayFilter(filters.FilterSet):
    pass


class DoctorScheduleDayViewSet(ModelViewSet):
    queryset = DoctorScheduleDay.objects.all()
    serializer_class = DoctorScheduleDayOtherSerializer
    # filterset_class = DoctorScheduleDayFilter
    filter_fields = "__all__"


class DoctorWorkShiftFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    week_day = filters.CharFilter(field_name="week_day__week_day")
    num_count = filters.NumberFilter(field_name="num_count")
    start_time = filters.TimeFilter(field_name="start_time", lookup_expr='gte')
    end_time = filters.TimeFilter(field_name="end_time", lookup_expr='lte')
    office_code = filters.CharFilter(field_name="office__codenum", lookup_expr='icontains')
    pb_type = filters.CharFilter(field_name="week_day__doctor_work_scheduling_main__pb_type")

    class Meta:
        model = DoctorWorkShift
        fields = "__all__"


class DoctorWorkShiftViewSet(ModelViewSet):
    queryset = DoctorWorkShift.objects.all().order_by('id')
    serializer_class = DoctorWorkShiftSerializer
    filterset_class = DoctorWorkShiftFilter
    filter_fields = "__all__"

    # 根据排班获取医院信息列表
    @action(methods=["GET"], detail=False)
    def hospitals(self, request):
        # work_date = request.query_params.get('work_date')
        # hospital_ids = DoctorWorkShift.objects.filter(
        #     work_date=work_date,
        # ).values_list('hospital_id', flat=True).annotate(office_count=Count('hospital'))
        # hospital_ids = list(hospital_ids)
        hospital_ids = self.filter_queryset(self.get_queryset()).distinct().values_list('hospital_id')
        hospitals = Hospital.objects.filter(id__in=hospital_ids)
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    # 根据排班获取科室信息列表
    @action(methods=["GET"], detail=False)
    def offices(self, request):
        # work_date = request.query_params.get('work_date')
        # hospital_id = request.query_params.get('hospital_id')
        # office_ids = DoctorWorkShift.objects.filter(
        #     work_date=work_date,
        #     hospital_id=hospital_id
        # ).values_list('office_id', flat=True).annotate(office_count=Count('office'))
        # office_ids = list(office_ids)
        office_ids = self.filter_queryset(self.get_queryset()).distinct().values_list('office_id')
        offices = Office.objects.filter(id__in=office_ids)
        serializer = OfficeSerializer(offices, many=True)
        return Response({'results': serializer.data})

    # 根据排班获取医生信息列表
    @action(methods=["GET"], detail=False)
    def doctors(self, request):
        fee_type = request.query_params.get('fee_type')
        doctor_ids = self.filter_queryset(self.get_queryset()).values_list('doctor_id')
        doctors = Doctor.objects.filter(id__in=doctor_ids)
        serializer = DoctorSerializer(doctors, many=True, context={'fee_type': fee_type})
        return Response({'results': serializer.data})


# def stop_diagnosis(request):
#     """停诊接口"""
#     """
#     1、根据相关信息查询排班记录
#     2、修改查询到的排班记录（将号源改为0？是否修改状态为休息？）
#     3、调用统一预约平台停诊接口（是否先写备注占位，之后再调用？）
#     5、根据相关信息查询到预约记录中该相关信息段中的患者预约记录
#     6、修改这些患者的预约状态（被停诊后的状态名怎么设定？）先设定6
#     7、并向其发送该医生停诊的消息（这块儿等集成im聊天后再实现？）
#     8、调用统一支付平台对其进行退费（是否先写备注占位，之后再调用？）
#     """
#     data = json.loads(request.body.decode('utf-8'))
#     ids = data['ids']
#     appoint_type = data['appoint_type']  # 预约类型： 1：在线、 2：门诊、 3：电话
#     """
#     2	下午	afternoon	t
#     3	晚上	night	t
#     1	上午	morning	t
#     """
#     time_interval = []
#     for id in ids:
#         doctor_workShift = DoctorWorkShift.objects.filter(id=int(id)).first()
#         ws_type = doctor_workShift.ws_type
#         work_date = doctor_workShift.work_date
#         doctor_workShift.is_active = True
#         doctor_workShift.num_count = 0
#         doctor_workShift.save()
#         data_dict = {"ws_type": ws_type.codenum, "work_date": work_date}
#         time_interval.append(data_dict)
#     """3、调用统一预约平台停诊接口（是否先写备注占位，之后再调用？）"""
#     list_code_pat = []
#     for item in time_interval:
#         list_appoint_record = AppointmentRecord.objects.filter(appoint_type=appoint_type,
#                                                                code_dayslottp=item['ws_type'],
#                                                                appoint_date=item['work_date'], is_active=True)
#         for record in list_appoint_record:
#             code_pat = record.code_pat
#             is_payment = record.is_payment
#             if is_payment:
#                 """
#                 8、调用统一支付平台对其进行退费（是否先写备注占位，之后再调用？）
#                  """
#                 pass
#             record.status = 6
#             record.save()
#             list_code_pat.append(code_pat)
#
#     for patient in set(list_code_pat):
#         """
#         7、并向其发送该医生停诊的消息（这块儿等集成im聊天后再实现？）
#         """
#         print(patient)
#
#     return JsonResponse("停诊成功", safe=False)


# def get_test():
#         print(121)
#         print(121)
#         print(121)
#         return "测试"


class ExportDoctorWorkSchedulingMainViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = DoctorWorkSchedulingMain.objects.all()
    serializer_class = ExportDoctorWorkSchedulingMainSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'doctor_work_scheduling_main.xlsx'
    # filterset_fields = {"name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "医生排班信息",
        'header_title': "医生排班信息",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    #
    # def custom_value_formatter(val):
    #     return val + '!!!'

    # def get_ws_doctor_schedule_days(self, obj):
    #     ws_doctor_schedule_days = obj.doctorscheduleday_set.all().order_by('week_day')
    #     data = DoctorScheduleDaySerializer(ws_doctor_schedule_days, many=True).data
    #     data_dict = dict(data)
    #     print(data_dict)
    #     # return {'data': DoctorScheduleDaySerializer(ws_doctor_schedule_days, many=True).data}
    #     return data_dict

    def get_test(self):
        print(121)
        print(121)
        print(121)
        return "测试"

    xlsx_custom_cols = {
        'my_custom_col.val1.title': {
            'label': '详细结果',
            # 'formatter': get_ws_doctor_schedule_days
            'formatter': get_test
        },
        'my_custom_col.val1.titles': {
            'label': '详细结果',
            # 'formatter': get_ws_doctor_schedule_days
            'formatter': get_test
        }
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


def import_doctor_work_scheduling(request):
    """导入医生排班excel表数据"""
    created_user = request.POST.get('created_user')
    pb_type = request.POST.get('pb_type')
    excel_file = request.FILES.get('excel_file', '')  # 获取前端上传的文件
    file_type = excel_file.name.split('.')[1].split('"')[0]  # 拿到文件后缀
    # file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    data_list = []
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        try:
            data = xlrd2.open_workbook(filename=None, file_contents=excel_file.read(), ragged_rows=True)
            sheets = data.sheets()
            for sheet in sheets:
                rows = sheet.nrows  # 总行数
                cols = sheet.ncols  # 总列数
                title_row = sheet.cell_value(0, 2)  # 首行的数据
                year = title_row.split('年')[0]
                month = title_row.split('年')[1].split('月')[0]
                moring_time = sheet.cell_value(0, 1)  # 上午上班的时间数据
                moring_split = moring_time.split('-')
                moring_start_str = moring_split[0]
                moring_start = datetime.strptime(moring_start_str, '%H:%M')
                moring_end_str = moring_split[1]
                moring_end = datetime.strptime(moring_end_str, '%H:%M')
                afternoon_time = sheet.cell_value(1, 1)  # 下午上班的时间数据
                afternoon_split = afternoon_time.split('-')
                afternoon_start_str = afternoon_split[0]
                afternoon_start = datetime.strptime(afternoon_start_str, '%H:%M')
                afternoon_end_str = afternoon_split[1]
                afternoon_end = datetime.strptime(afternoon_end_str, '%H:%M')
                evening_time = sheet.cell_value(2, 1)  # 晚上上班的时间数据
                evening_split = evening_time.split('-')
                evening_start_str = evening_split[0]
                evening_start = datetime.strptime(evening_start_str, '%H:%M')
                evening_end_str = evening_split[1]
                evening_end = datetime.strptime(evening_end_str, '%H:%M')
                start_day = sheet.cell_value(4, 6)  # 起始day的数据
                start_time_str = year + month + str(int(start_day))
                start_time = datetime.strptime(start_time_str, '%Y%m%d')

                for row in range(5, rows, 3):  # 从5开始是为了去掉表头,每次跳过三行数据循环一次
                    order_num = sheet.cell_value(row, 0)  # 序号
                    hospital_name = sheet.cell_value(row, 1)  # 医院名称
                    if hospital_name:
                        hospital = Hospital.objects.get(name=hospital_name).id
                    else:
                        break
                    office_name = sheet.cell_value(row, 2)  # 科室名称
                    if office_name:
                        office = Office.objects.get(name=office_name, hospital_id=hospital).id
                    job_number = sheet.cell_value(row, 3)  # 医生工号
                    if job_number:
                        doctor = Doctor.objects.get(job_number=str(int(job_number)), office_id=office, hospital_id=hospital)

                    exist_doctor_work_scheduling_main = DoctorWorkSchedulingMain.objects.filter(hospital_id=hospital,
                                                                                                office_id=office,
                                                                                                doctor_id=doctor.id,
                                                                                                start_time=start_time,
                                                                                                pb_type=pb_type,
                                                                                                ).first()
                    if exist_doctor_work_scheduling_main:
                        excel_data = {
                            "order_num": order_num,
                            "doctor_work_scheduling_main_id": None,
                            "hospital_name": hospital_name,
                            "office_name": office_name,
                            "job_number": job_number,
                            "doctor_name": doctor.name,
                            "done": '序号为' + str(order_num) + '的记录已存在，已为您跳过该条导入！！！',
                        }
                        data_list.append(excel_data)
                        continue
                    else:
                        doctor_work_scheduling_main = DoctorWorkSchedulingMain.objects.create(
                            name='文件导入',
                            hospital_id=hospital,
                            office_id=office,
                            doctor_id=doctor.id,
                            pb_type=pb_type,
                            created_by_id=created_user,
                            updated_by_id=created_user,
                            start_time=start_time,
                        )
                        for col in range(6, cols):
                            row_week = sheet.cell_value(3, col)  # 周几
                            day = sheet.cell_value(4, col)  # day的数据
                            week_dict = {'一': 1,
                                         '二': 2,
                                         '三': 3,
                                         '四': 4,
                                         '五': 5,
                                         '六': 6,
                                         '日': 7}
                            str_date = year + month + str(int(day))
                            work_date = datetime.strptime(str_date, '%Y%m%d')
                            # print(datetime.strptime(str_date, '%Y%m%d'))
                            # print(datetime.strptime('8:30', '%H:%M'))
                            doctor_schedule_day = DoctorScheduleDay.objects.create(
                                week_day=week_dict[row_week],
                                work_date=work_date,
                                doctor_id=doctor.id,
                                doctor_work_scheduling_main_id=doctor_work_scheduling_main.id
                            )
                            moring_value = sheet.cell_value(row, col)  # 上午的数据
                            moring_is_active = False
                            if moring_value == '休':
                                moring_value = 0
                                moring_is_active = True
                            doctor_work_shift = DoctorWorkShift.objects.create(
                                name='上午',
                                week_day_id=doctor_schedule_day.id,
                                start_time=moring_start,
                                end_time=moring_end,
                                num_count=moring_value,
                                left_num=moring_value,
                                is_active=moring_is_active,
                                work_date=work_date,
                                hospital_id=hospital,
                                office_id=office,
                                doctor_id=doctor.id,
                                ws_type_id=1,
                            )

                            afternoon_value = sheet.cell_value(row + 1, col)  # 下午的数据
                            afternoon_is_active = False
                            if afternoon_value == '休':
                                afternoon_value = 0
                                afternoon_is_active = True
                            doctor_work_shift = DoctorWorkShift.objects.create(
                                name='下午',
                                week_day_id=doctor_schedule_day.id,
                                start_time=afternoon_start,
                                end_time=afternoon_end,
                                num_count=afternoon_value,
                                left_num=afternoon_value,
                                is_active=afternoon_is_active,
                                work_date=work_date,
                                hospital_id=hospital,
                                office_id=office,
                                doctor_id=doctor.id,
                                ws_type_id=2,
                            )

                            evening_value = sheet.cell_value(row + 2, col)  # 晚上的数据
                            evening_is_active = False
                            if evening_value == '休':
                                evening_value = 0
                                evening_is_active = True
                            doctor_work_shift = DoctorWorkShift.objects.create(
                                name='晚上',
                                week_day_id=doctor_schedule_day.id,
                                start_time=evening_start,
                                end_time=evening_end,
                                num_count=evening_value,
                                left_num=evening_value,
                                is_active=evening_is_active,
                                work_date=work_date,
                                hospital_id=hospital,
                                office_id=office,
                                doctor_id=doctor.id,
                                ws_type_id=3,
                            )
                        excel_data = {
                            "order_num": order_num,
                            "doctor_work_scheduling_main_id": doctor_work_scheduling_main.id,
                            "hospital_name": hospital_name,
                            "office_name": office_name,
                            "job_number": job_number,
                            "doctor_name": doctor.name,
                            "done": title_row,
                        }
                        data_list.append(excel_data)
        except Exception as e:
            raise e

    if data_list:
        res = {"data": data_list}
    else:
        res = {"data": "文件内容格式有误，请检查内容格式是否正确！"}
    return JsonResponse(res)
