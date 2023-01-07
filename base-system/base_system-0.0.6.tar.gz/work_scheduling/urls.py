"""MedicalSystem URL Configuration

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
from base_system.viewset import group_viewset, permission_viewset
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    # path('login/',views.login),
    # path('stop_dignosis/', views.stop_diagnosis),  # 停诊接口

    path('import_dws/', views.import_doctor_work_scheduling),  # 导入医生排班excel表数据

]
router = routers.DefaultRouter()
router.register(r'worksche', views.WorkSchedulingMainViewSet)
router.register(r'worksche_doctor', views.WorkSchedulingMainDoctorViewSet)
router.register(r'doctor_worksche', views.DoctorWorkSchedulingMainViewSet)
router.register(r'ws_work_shift_type', views.WorkShiftTypeViewSet)

router.register(r'drsddays', views.DoctorScheduleDayViewSet)  # 医生排班
router.register(r'apn', views.DoctorWorkShiftViewSet)  # 排班相关viewset

router.register(r'export_doctor_work', views.ExportDoctorWorkSchedulingMainViewSet)  # 医生排班信息导出接口（存在问题）




urlpatterns += router.urls
