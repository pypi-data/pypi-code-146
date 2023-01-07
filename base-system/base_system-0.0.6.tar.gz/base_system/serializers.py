from django.contrib.auth.models import Permission
from rest_framework import serializers
from base_system.models import Hospital, Office, Doctor, PositionTitle, User, ExtraGroup, InspectionDictionaries, \
    ExaminationDictionaries, DrugDirectory, DrugCategory, DrugPreparationType, PharmacyManagement


class PermissionSerializer(serializers.ModelSerializer):
    """
    操作权限
    """

    class Meta:
        model = Permission
        fields = "__all__"


class PasswordSerializer(serializers.Serializer):
    origin_password = serializers.CharField(required=False)
    password = serializers.CharField(min_length=6, max_length=18)
    password2 = serializers.CharField(min_length=6, max_length=18)  # 确认密码

    class Meta:
        fields = ["password", 'password2']

    def validate_origin_password(self, value):
        user = self.context["request"].user
        if user.is_superuser:
            # 如果是超级管理员，可以更改其他人的密码
            return value
        if not user.check_password(value):
            raise serializers.ValidationError("原密码不正确")
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:  # 防止为空
            raise serializers.ValidationError("两次密码不一致")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    电子地图上标识的位置信息
    """

    # groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        # groups = validated_data.pop("groups")
        # parts = validated_data.pop("parts_up")
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        # # if parts:
        # #     # validated_data['default_part_id'] = list(parts)[0]
        # #     user.default_part_id = list(parts)[0]
        # if groups:
        #     user.default_group_id = list(groups)[0]
        user.save()
        # # user.parts.set(parts)
        # user.groups.set(groups)
        # user.save()
        return user


class ExportHospitalSerializer(serializers.ModelSerializer):
    '''
    导出医院序列化器
    '''
    parent = serializers.SerializerMethodField(label=('上级医院'))

    class Meta:
        model = Hospital
        # fields = "__all__"
        fields = (
            'codenum',
            'name',
            'parent',
            'address',
            'longitude',
            'latitude',
            'phone',
            'introduce',
            'created_time',
            'created_by',
        )

    def get_parent(self, obj):
        parent = obj.parent
        if parent:
            return parent.name


class ExportOfficeSerializer(serializers.ModelSerializer):
    '''
    导出科室序列化器
    '''
    hospital = serializers.SerializerMethodField(label=('所属医院'))
    parent = serializers.SerializerMethodField(label=('上级科室'))

    class Meta:
        model = Office
        # fields = "__all__"
        fields = (
            'codenum',
            'name',
            'hospital',
            'parent',
            'address',
            'phone',
            'introduce',
            'created_time',
            'created_by',
        )

    def get_hospital(self, obj):
        return obj.hospital.name

    def get_parent(self, obj):
        parent = obj.parent
        if parent:
            return parent.name


class ExportDoctorSerializer(serializers.ModelSerializer):
    '''
    导出医生序列化器
    '''
    hospital = serializers.SerializerMethodField(label=('所属医院'))
    office = serializers.SerializerMethodField(label=('所属科室'))
    doc_rank = serializers.SerializerMethodField(label=('医生职称'))

    class Meta:
        model = Doctor
        # fields = "__all__"
        fields = (
            'hospital',
            'office',
            'job_number',
            'name',
            'doc_rank',
            'describe',
            'is_online_consult',
        )

    def get_hospital(self, obj):
        hospital = obj.hospital
        if hospital:
            return hospital.name

    def get_office(self, obj):
        office = obj.office
        if office:
            return office.name

    def get_doc_rank(self, obj):
        doc_rank = obj.doc_rank
        if doc_rank:
            return doc_rank.name


class ExportPositionTitleSerializer(serializers.ModelSerializer):
    '''
    导出职称序列化器
    '''
    hospital = serializers.SerializerMethodField(label=('所属医院'))

    class Meta:
        model = PositionTitle
        # fields = "__all__"
        fields = (
            'codenum',
            'name',
            'hospital',
            'created_time',
            'created_by',
        )

    def get_hospital(self, obj):
        return obj.hospital.name


class ExportGroupSerializer(serializers.ModelSerializer):
    '''
    导出角色序列化器
    '''
    hospital = serializers.SerializerMethodField(label=('所属医院'))
    extra_group = serializers.SerializerMethodField(label=('角色名称'))

    class Meta:
        model = ExtraGroup
        # fields = "__all__"
        fields = (
            'role_code',
            'extra_group',
            'is_active',
            'hospital',
            'created_user',
            'created_at',
        )

    def get_hospital(self, obj):
        return obj.hospital.name

    def get_extra_group(self, obj):
        return obj.group.name


class InspectionDictionariesSerializer(serializers.ModelSerializer):
    """检查字典序列化器"""
    hospital_name = serializers.SerializerMethodField()
    office_name = serializers.SerializerMethodField()

    class Meta:
        model = InspectionDictionaries
        fields = "__all__"

    def get_hospital_name(self, obj):
        hospital = Hospital.objects.filter(codenum=obj.hospital_code).first()
        return hospital.name

    def get_office_name(self, obj):
        office = Office.objects.filter(codenum=obj.office_code).first()
        return office.name


class ExportInspectionDictionariesSerializer(serializers.ModelSerializer):
    """导出检查字典序列化器"""
    hospital_name = serializers.SerializerMethodField(label='所属医院')
    office_name = serializers.SerializerMethodField(label='所属科室')

    class Meta:
        model = InspectionDictionaries
        fields = (
            'project_code',
            'project_name',
            'hospital_name',
            'office_name',
            'project_fees',
            'remarks'
        )

    def get_hospital_name(self, obj):
        hospital = Hospital.objects.filter(codenum=obj.hospital_code).first()
        return hospital.name

    def get_office_name(self, obj):
        office = Office.objects.filter(codenum=obj.office_code).first()
        return office.name


class ExaminationDictionariesSerializer(serializers.ModelSerializer):
    """检验字典序列化器"""
    hospital_name = serializers.SerializerMethodField()
    office_name = serializers.SerializerMethodField()

    class Meta:
        model = ExaminationDictionaries
        fields = "__all__"

    def get_hospital_name(self, obj):
        hospital = Hospital.objects.filter(codenum=obj.hospital_code).first()
        return hospital.name

    def get_office_name(self, obj):
        office = Office.objects.filter(codenum=obj.office_code).first()
        return office.name


class ExportExaminationDictionariesSerializer(serializers.ModelSerializer):
    """导出检验字典序列化器"""
    hospital_name = serializers.SerializerMethodField(label='所属医院')
    office_name = serializers.SerializerMethodField(label='所属科室')

    class Meta:
        model = ExaminationDictionaries
        fields = (
            'project_code',
            'project_name',
            'hospital_name',
            'office_name',
            'project_fees',
            'remarks'
        )

    def get_hospital_name(self, obj):
        hospital = Hospital.objects.filter(codenum=obj.hospital_code).first()
        return hospital.name

    def get_office_name(self, obj):
        office = Office.objects.filter(codenum=obj.office_code).first()
        return office.name


class ExportDrugDirectorySerializer(serializers.ModelSerializer):
    """导出药品目录序列化器"""

    preparation_type_name = serializers.SerializerMethodField(label='制剂类型')
    category_name = serializers.SerializerMethodField(label='分类')

    class Meta:
        model = DrugDirectory
        fields = (
            'drug_code',
            'drug_name',
            'standards',
            'units',
            'preparation_type_name',
            'category_name',
            'origin_place',
            'manufacturer',
            'price'
        )

    def get_preparation_type_name(self, obj):
        return obj.preparation_type.type_name

    def get_category_name(self, obj):
        return obj.category.category_name


class PharmacyManagementSerializer(serializers.ModelSerializer):
    """药房管理序列化器"""
    belong_unit = serializers.SerializerMethodField()

    class Meta:
        model = PharmacyManagement
        fields = (
            'pharmacy_code',
            'pharmacy_name',
            'pharmacy_type',
            'address',
            'belong_unit',
            'is_active',
        )
        depth = 2

    def get_belong_unit(self, obj):
        if obj.pharmacy_type.id == 1:
            return obj.hospital.name
        elif obj.pharmacy_type.id == 2:
            return obj.enterprise.name


class ExportUserSerializer(serializers.ModelSerializer):
    '''
    导出用户序列化器
    '''
    hospital = serializers.SerializerMethodField(label=('所属医院'))
    office = serializers.SerializerMethodField(label=('所属科室'))
    user_rank = serializers.SerializerMethodField(label=('职级'))
    doctor = serializers.SerializerMethodField(label=('绑定医生'))
    is_online_consult = serializers.SerializerMethodField(label=('是否互联网接诊'))
    groups = serializers.SerializerMethodField(label=('用户角色'))

    class Meta:
        model = User
        # fields = "__all__"
        fields = (
            'hospital',
            'office',
            'doctor',
            'user_rank',
            'username',
            'password',
            'is_online_consult',
            'groups',
        )

    def get_groups(self, obj):
        groups = obj.groups.all()
        role_list = [group.name for group in groups if groups]
        role_str = ",".join(role_list)
        return role_str

    def get_hospital(self, obj):
        hospital = obj.hospital
        if hospital:
            return hospital.name

    def get_office(self, obj):
        office = obj.office
        if office:
            return office.name

    def get_user_rank(self, obj):
        user_rank = obj.user_rank
        if user_rank:
            return user_rank.name

    def get_doctor(self, obj):
        doctor = obj.doctor
        if doctor:
            return doctor.name

    def get_is_online_consult(self, obj):
        doctor = obj.doctor
        if doctor:
            return doctor.is_online_consult
