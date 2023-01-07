from rest_framework import serializers

from base_system.models import Hospital, Office, Doctor, ExpenseStandard


class HospitalSerializer(serializers.ModelSerializer):
    """
    医院信息序列化器
    """
    class Meta:
        model = Hospital
        fields = "__all__"


class OfficeSerializer(serializers.ModelSerializer):
    """
    科室信息序列化器
    """
    class Meta:
        model = Office
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    """
    医生信息序列化器
    """
    position_name = serializers.SerializerMethodField()
    office_code = serializers.SerializerMethodField()
    office_name = serializers.SerializerMethodField()
    hospital_code = serializers.SerializerMethodField()
    hospital_name = serializers.SerializerMethodField()
    doctor_fee = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = "__all__"

    def get_position_name(self, obj):
        return obj.doc_rank.name

    def get_office_code(self, obj):
        return obj.office.codenum

    def get_office_name(self, obj):
        return obj.office.name

    def get_hospital_code(self, obj):
        return obj.hospital.codenum

    def get_hospital_name(self, obj):
        return obj.hospital.name

    def get_doctor_fee(self, obj):
        drfees = obj.expensestandard_set.all()
        if 'fee_type' in self.context.keys():
            fee_type = self.context['fee_type']
            doctor_fee = drfees.filter(expense_type=fee_type).first()
            if doctor_fee:
                return doctor_fee.fees
        else:
            # dr_fee = ExpenseStandard.objects.filter(doctors=obj.id)
            serializer = ExpenseStandardSerializer(drfees, many=True)
            return serializer.data


class ExpenseStandardSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseStandard
        fields = "__all__"
