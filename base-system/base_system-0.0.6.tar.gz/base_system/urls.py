"""Infrastructure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views
from base_system.views import PermissionsView
from base_system.viewset import group_viewset, permission_viewset, appointment_viewset
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    # path('login/',views.login),
    path('register/', views.register),
    path('login/', obtain_jwt_token),  # 登录
    path('token/refresh/', refresh_jwt_token),
    path('verify/', verify_jwt_token),
    path('permissions/', PermissionsView.as_view(), name='permissions'),
    path('change-password/', views.change_password),
    path('all-permissions/', group_viewset.all_permissions),  # 获取系统所有权限
    path('own-menu/', group_viewset.get_own_permissions),  # 获取系统所有权限
    path('import_position_title/', views.import_position_title),  # 职称信息导入接口
    path('import_office/', views.import_office),  # 科室信息导入接口
    path('import_doctor/', views.import_doctor),  # 医生信息导入接口
    path('menu_permissions/', permission_viewset.menu_permissions),
]
router = routers.DefaultRouter()
router.register(r'export_hospital', views.HospitalInfoExportViewSet)  # 医院信息导出接口
router.register(r'export_office', views.OfficeInfoExportViewSet)  # 科室信息导出接口
router.register(r'export_group', views.GroupExportViewSet)  # 角色信息导出接口
router.register(r'export_doctor', views.DoctorInfoExportViewSet)  # 医生信息导出接口
router.register(r'export_user', views.UserInfoExportViewSet)  # 用户信息导出接口
router.register(r'groups', group_viewset.GroupViewSet)  # 角色
router.register(r'users', views.UserViewSet)  # 用户信息
router.register(r'ins_dic', views.InspectionDictionariesViewSet)  # 检查字典
router.register(r'export_ins_dic', views.InspectionDictionariesInfoExportViewSet)  # 导出检查字典
router.register(r'exa_dic', views.ExaminationDictionariesViewSet)  # 检验字典
router.register(r'export_exa_dic', views.ExaminationDictionariesInfoExportViewSet)  # 导出检验字典
router.register(r'export_drug_directory', views.DrugDirectoryExportViewSet)  # 导出药品目录
router.register(r'pharmacy_management', views.PharmacyManagementViewSet)  # 药房管理

# 预约相关
router.register(r'hospitals', appointment_viewset.HospitalViewSet)
router.register(r'offices', appointment_viewset.OfficeViewSet)
router.register(r'doctors', appointment_viewset.DoctorViewSet)

urlpatterns += router.urls
