from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from django_k8s_health_check.settings import api_settings
from django_k8s_health_check.utils import HealthCheck


class HealthView(GenericAPIView):

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        data, has_erro = self.mount_response_data()
        return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR if has_erro else HTTP_200_OK)

    def mount_response_data(self):
        data, has_error = {}, False

        if api_settings.SERVICE_NAME:
            data['service'] = api_settings.SERVICE_NAME

        if api_settings.SERVICE_VERSION:
            data['version'] = api_settings.SERVICE_VERSION

        if api_settings.CHECK_DATABASE:
            db_error, data['databases'] = HealthCheck.test_databases()
            has_error = not has_error and not db_error

        if api_settings.CHECK_CACHE:
            cache_error, data['caches'] = HealthCheck.test_caches()
            has_error = not has_error and not cache_error

        return data, has_error
