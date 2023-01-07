from rest_framework import serializers
from .models import WorkSchedulingMain, ScheduleDay, WorkShift, WorkShiftType, DoctorWorkSchedulingMain, \
    DoctorScheduleDay, DoctorWorkShift
from rest_framework.utils import model_meta


class WorkSchedulingMainSerializer(serializers.ModelSerializer):
    """
    操作权限
    """
    ws_schedule_days = serializers.SerializerMethodField()

    class Meta:
        model = WorkSchedulingMain
        fields = "__all__"

    def get_ws_schedule_days(self, obj):
        ws_schedule_days = obj.scheduleday_set.all().order_by('week_day')
        return {'data': ScheduleDaySerializer(ws_schedule_days, many=True).data}

    def update(self, instance, validated_data):
        # raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)
        data_schedule_days = self.context['ws_schedule_days']['data']
        ins_schedule_days = instance.scheduleday_set.all()
        ins_schedule_days = list(ins_schedule_days)
        for detail_data in data_schedule_days:
            detail = ins_schedule_days.pop(0)
            ws_work_shifts = detail_data['ws_work_shifts']
            sch_day_ser = ScheduleDaySerializer(detail, data=detail_data, context={'ws_work_shifts': ws_work_shifts})
            sch_day_ser.is_valid(raise_exception=True)
            # print(sch_day_ser.data)
            sch_day_ser.save()

        return instance


class WorkSchedulingMainDoctorSerializer(serializers.ModelSerializer):
    """
    医生排班模板主表
    """
    ws_doctor_schedule_days = serializers.SerializerMethodField()

    class Meta:
        model = WorkSchedulingMain
        fields = "__all__"

    def get_ws_doctor_schedule_days(self, obj):
        ws_schedule_days = obj.scheduleday_set.all().order_by('week_day')
        return {'data': ScheduleDayDoctorSerializer(ws_schedule_days, many=True).data}

    def update(self, instance, validated_data):
        data_schedule_days = validated_data.pop('data_schedule_days')
        # print(instance)
        ins_schedule_days = instance.scheduleday.all()
        ins_schedule_days = list(ins_schedule_days)
        for detail_data in data_schedule_days:
            detail = ins_schedule_days.pop(0)
            ScheduleDaySerializer(detail, data=detail_data)

        return instance


class ScheduleDayDoctorSerializer(serializers.ModelSerializer):
    """
    排班日期
    """
    ws_doctor_work_shifts = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleDay
        fields = "__all__"

    def get_ws_doctor_work_shifts(self, obj):
        ws_work_shifts = obj.workshift_set.all().order_by('ws_type')
        return {'data': WorkShiftSerializer(ws_work_shifts, many=True).data}


class ScheduleDaySerializer(serializers.ModelSerializer):
    """
    操作权限
    """
    ws_work_shifts = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleDay
        fields = "__all__"

    def get_ws_work_shifts(self, obj):
        ws_work_shifts = obj.workshift_set.all().order_by('ws_type')
        return {'data': WorkShiftSerializer(ws_work_shifts, many=True).data}

    def update(self, instance, validated_data):
        #
        for attr, value in validated_data.items():
            print(attr, value)
            setattr(instance, attr, value)
        print(instance)
        instance.save()

        ws_work_shifts = self.context['ws_work_shifts']['data']
        print(333333, ws_work_shifts)
        ins_work_shifts = instance.workshift_set.all()
        ins_work_shifts = list(ins_work_shifts)
        for detail_data in ws_work_shifts:
            detail = ins_work_shifts.pop(0)
            ser_shift = WorkShiftSerializer(detail, data=detail_data)
            ser_shift.is_valid()
            ser_shift.save()

        return instance


class WorkShiftSerializer(serializers.ModelSerializer):
    """
    操作权限
    """
    ws_type_id = serializers.SerializerMethodField()

    class Meta:
        model = WorkShift
        fields = "__all__"

    def get_ws_type_id(self, obj):
        return obj.ws_type.id


class WorkShiftTypeSerializer(serializers.ModelSerializer):
    """
    操作权限
    """

    class Meta:
        model = WorkShiftType
        fields = "__all__"


class DoctorWorkSchedulingMainSerializer(serializers.ModelSerializer):
    """
    操作权限
    """
    ws_doctor_schedule_days = serializers.SerializerMethodField()
    hospital_name = serializers.SerializerMethodField()
    office_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = DoctorWorkSchedulingMain
        fields = "__all__"

    def get_ws_doctor_schedule_days(self, obj):
        ws_doctor_schedule_days = obj.doctorscheduleday_set.all().order_by('week_day')
        return {'data': DoctorScheduleDaySerializer(ws_doctor_schedule_days, many=True).data}

    def get_hospital_name(self, obj):
        return obj.hospital.name

    def get_office_name(self, obj):
        return obj.office.name

    def get_doctor_name(self, obj):
        return obj.doctor.name

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            print(attr, value)
            setattr(instance, attr, value)
        print(instance)
        instance.save()
        data_schedule_days = self.context['ws_doctor_schedule_days']['data']
        ins_schedule_days = instance.doctorscheduleday_set.all()
        ins_schedule_days = list(ins_schedule_days)
        for detail_data in data_schedule_days:
            detail = ins_schedule_days.pop(0)
            ws_doctor_work_shifts = detail_data['ws_doctor_work_shifts']
            sch_day_ser = DoctorScheduleDaySerializer(detail, data=detail_data,
                                                      context={'ws_doctor_work_shifts': ws_doctor_work_shifts})
            sch_day_ser.is_valid(raise_exception=True)
            # print(sch_day_ser.data)
            sch_day_ser.save()

        return instance


class DoctorScheduleDaySerializer(serializers.ModelSerializer):
    """
    医生排班日期
    """
    ws_doctor_work_shifts = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = DoctorScheduleDay
        fields = "__all__"

    def get_ws_doctor_work_shifts(self, obj):
        ws_work_shifts = obj.doctorworkshift_set.all().order_by('ws_type')
        return {'data': DoctorWorkShiftSerializer(ws_work_shifts, many=True).data}

    def get_doctor_name(self, obj):
        return obj.doctor.name

    def update(self, instance, validated_data):
        #
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        ws_work_shifts = self.context['ws_doctor_work_shifts']['data']
        ins_work_shifts = instance.doctorworkshift_set.all()
        ins_work_shifts = list(ins_work_shifts)
        for detail_data in ws_work_shifts:
            detail = ins_work_shifts.pop(0)
            ser_shift = DoctorWorkShiftSerializer(detail, data=detail_data)
            ser_shift.is_valid()
            ser_shift.save()

        return instance


class DoctorWorkShiftSerializer(serializers.ModelSerializer):
    """
    医生排班班次
    """
    ws_type_id = serializers.SerializerMethodField()

    class Meta:
        model = DoctorWorkShift
        fields = "__all__"

    def get_ws_type_id(self, obj):
        return obj.ws_type.id


class DoctorScheduleDayOtherSerializer(serializers.ModelSerializer):
    """
    医生排班日期
    """
    doctor_work_shifts = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = DoctorScheduleDay
        fields = "__all__"

    def get_doctor_work_shifts(self, obj):
        ws_work_shifts = obj.doctorworkshift_set.all().order_by('ws_type')
        ser_data = DoctorWorkShiftSerializer(ws_work_shifts, many=True).data
        return ser_data

    def get_doctor_name(self, obj):
        return obj.doctor.name


class ExportDoctorWorkSchedulingMainSerializer(serializers.ModelSerializer):
    """
    导出排班序列化器
    """
    # ws_doctor_schedule_days = serializers.SerializerMethodField(label='详细排班')
    hospital_name = serializers.SerializerMethodField(label='所属医院')
    office_name = serializers.SerializerMethodField(label='所属科室')
    doctor_name = serializers.SerializerMethodField(label='所属医生')

    class Meta:
        model = DoctorWorkSchedulingMain
        # fields = "__all__"
        fields = (
            'hospital_name',
            'office_name',
            'doctor_name',
            # 'ws_doctor_schedule_days',
        )

    # def get_ws_doctor_schedule_days(self, obj):
    #     ws_doctor_schedule_days = obj.doctorscheduleday_set.all().order_by('week_day')
    #     data_dict = DoctorScheduleDaySerializer(ws_doctor_schedule_days, many=True).data
    #     print(data_dict, type(data_dict))
    #     return {'data': DoctorScheduleDaySerializer(ws_doctor_schedule_days, many=True).data}

    def get_hospital_name(self, obj):
        return obj.hospital.name

    def get_office_name(self, obj):
        return obj.office.name

    def get_doctor_name(self, obj):
        return obj.doctor.name



