# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoK8sHealthCheck(AppConfig):
    name = 'django_k8s_health_check'
    verbose_name = _('Django Health Check')
