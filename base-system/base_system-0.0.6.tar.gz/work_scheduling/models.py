from django.db import models
from base_system.models import MedicalBaseModel, Hospital, Office, Doctor
from django.conf import settings as django_settings

AUTH_USER_MODEL = getattr(django_settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.


class AppointmentTypeName(MedicalBaseModel):
    name = models.CharField(verbose_name="名称", max_length=255)
    code = models.CharField(verbose_name="编码", max_length=255)

    class Meta:
        db_table = "ws_appointment_type_name"
        verbose_name = "预约参数名称"
        verbose_name_plural = verbose_name


class AppointmentParameterSetting(MedicalBaseModel):
    name = models.CharField(verbose_name="名称", max_length=255)
    hospital = models.ForeignKey(
        Hospital,
        verbose_name="所属医院",
        on_delete=models.CASCADE,
    )
    # appointment_type = models.IntegerField(verbose_name='预约类型', null=True, blank=True)
    appointment_type = models.ForeignKey(
        AppointmentTypeName,
        verbose_name="类型名称",
        on_delete=models.CASCADE
    )

    appoint_advance = models.FloatField(verbose_name='提前预约时长', null=True, blank=True)
    appoint_over_time_refer = models.CharField(verbose_name='预约截止时间参照（是参照开始时间还是结束时间',
                                               max_length=100,
                                               null=True,
                                               blank=True,
                                               )
    appoint_over_time_type = models.CharField(verbose_name='预约截止时间与参照时间对比是提前还是推迟',
                                              max_length=100,
                                              null=True,
                                              blank=True,
                                              )

    appoint_over_time = models.CharField(verbose_name='预约截止时间时长', max_length=100, null=True, blank=True)
    cancel_time_refer = models.CharField(verbose_name='取消预约截止时间参照（是参照开始时间还是结束时间',
                                         max_length=100,
                                         null=True,
                                         blank=True,
                                         )
    cancel_time_type = models.CharField(
        verbose_name='取消预约截止时间与参照时间对比是提前还是推迟',
        max_length=100,
        null=True,
        blank=True,
    )
    cancel_time = models.CharField(verbose_name='取消预约截止时间', max_length=100, null=True, blank=True)

    class Meta:
        db_table = "ws_appointment_parameter_setting"
        verbose_name = "预约参数配置"
        verbose_name_plural = verbose_name


class WorkShiftType(models.Model):
    name = models.CharField(verbose_name="名称", max_length=200)
    codenum = models.CharField(verbose_name="编码", max_length=200, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        db_table = "ws_work_shift_type"
        verbose_name = "排班类型"
        verbose_name_plural = verbose_name


class WorkSchedulingMain(MedicalBaseModel):
    name = models.CharField(verbose_name="名称", max_length=255)
    hospital = models.ForeignKey(
        Hospital,
        verbose_name="所属医院",
        on_delete=models.CASCADE,
    )
    office = models.ForeignKey(
        Office,
        verbose_name="所属科室",
        on_delete=models.CASCADE,
        null=True
    )
    created_by = models.CharField(verbose_name="创建人", max_length=100, null=True, blank=True)
    updated_by = models.CharField(verbose_name="更新人", max_length=100, null=True, blank=True)
    ws_type = models.CharField(
        verbose_name="排班类型",
        max_length=4,
        choices=(
            ('1', "医生排班"),
            ('2', "在线问诊排班"),
            ('3', "电话问诊排班"),
        ),
        null=True
    )

    class Meta:
        db_table = "ws_work_scheduling_main"
        verbose_name = "排班模板主表"
        verbose_name_plural = verbose_name


class ScheduleDay(models.Model):
    week_day = models.IntegerField(verbose_name='周几', null=True, blank=True)
    work_scheduling_main = models.ForeignKey(
        WorkSchedulingMain,
        verbose_name="所属排班主",
        on_delete=models.CASCADE,
        null=True
    )
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        db_table = "ws_schedule_day"
        verbose_name = "排班日期"
        verbose_name_plural = verbose_name


class WorkShift(models.Model):
    name = models.CharField(verbose_name="名称", max_length=255)
    week_day = models.ForeignKey(
        ScheduleDay,
        verbose_name='周几',
        on_delete=models.CASCADE,
        null=True
    )
    start_time = models.TimeField(verbose_name='开始时间', null=True)
    end_time = models.TimeField(verbose_name='截至时间', null=True)
    num_count = models.IntegerField(verbose_name='号源', null=True, blank=True)
    ws_type = models.ForeignKey(
        WorkShiftType,
        verbose_name="排班类型",
        on_delete=models.CASCADE,
        null=True
    )
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        db_table = "ws_work_shift"
        verbose_name = "排班班次"
        verbose_name_plural = verbose_name


class DoctorWorkSchedulingMain(MedicalBaseModel):
    name = models.CharField(verbose_name="名称", max_length=255)
    hospital = models.ForeignKey(
        Hospital,
        verbose_name="所属医院",
        on_delete=models.CASCADE,
    )
    office = models.ForeignKey(
        Office,
        verbose_name="所属科室",
        on_delete=models.CASCADE,
        null=True
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        null=True
    )
    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="创建人",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='createduser'
    )
    updated_by = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="更新人",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='updateduser'
    )
    pb_type = models.CharField(
        verbose_name="排班类型",
        max_length=4,
        choices=(
            ('1', "医生排班"),
            ('2', "电话问诊排班"),
            ('3', "在线问诊排班"),
        ),
        null=True
    )
    start_time = models.DateField(verbose_name='起始日期', null=True)

    class Meta:
        db_table = "ws_doctor_work_scheduling_main"
        verbose_name = "医生排班模板主表"
        verbose_name_plural = verbose_name


class DoctorScheduleDay(models.Model):
    week_day = models.IntegerField(verbose_name='周几', null=True, blank=True)
    work_date = models.DateField(verbose_name='日期', auto_now_add=True, null=True)
    doctor_work_scheduling_main = models.ForeignKey(
        DoctorWorkSchedulingMain,
        verbose_name="所属排班医生",
        on_delete=models.CASCADE,
        null=True
    )
    is_active = models.BooleanField(verbose_name="是否启用", default=True)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        db_table = "ws_doctor_schedule_day"
        verbose_name = "医生排班日期"
        verbose_name_plural = verbose_name


class DoctorWorkShift(models.Model):
    name = models.CharField(verbose_name="名称", max_length=255)
    week_day = models.ForeignKey(
        DoctorScheduleDay,
        verbose_name='周几',
        on_delete=models.CASCADE,
        null=True
    )
    start_time = models.TimeField(verbose_name='开始时间', null=True)
    end_time = models.TimeField(verbose_name='截至时间', null=True)
    num_count = models.IntegerField(verbose_name="号源", null=True, blank=True)
    left_num = models.IntegerField(verbose_name="余号", null=True)
    work_date = models.DateField(verbose_name='日期', null=True)
    ws_type = models.ForeignKey(
        WorkShiftType,
        verbose_name="排班类型",
        on_delete=models.CASCADE,
        null=True
    )
    doctor = models.ForeignKey(
        Doctor,
        verbose_name="所属医生",
        on_delete=models.CASCADE,
        null=True
    )
    office = models.ForeignKey(
        Office,
        verbose_name="所属科室",
        on_delete=models.CASCADE,
        null=True
    )
    hospital = models.ForeignKey(
        Hospital,
        verbose_name="所属医院",
        on_delete=models.CASCADE,
        null=True
    )
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        db_table = "ws_doctor_work_shift"
        verbose_name = "医生排班班次"
        verbose_name_plural = verbose_name
