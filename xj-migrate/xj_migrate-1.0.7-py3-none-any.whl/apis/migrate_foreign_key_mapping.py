# _*_coding:utf-8_*_

import logging

from rest_framework import generics
from rest_framework.response import Response

from ..services.migrate_foregin_key_mapping_service import MigrateForeignKeyMappingService
from ..utils.model_handle import parse_data, util_response

logger = logging.getLogger(__name__)


# 迁移键名映射
class MigrateForeignKeyMapping(generics.UpdateAPIView):  # 或继承(APIView)

    def get(self, request, *args, **kwargs):
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': MigrateForeignKeyMappingService.get()
        })

    def post(self, request, *args, **kwargs):
        params = parse_data(request)
        if not params:
            return util_response(err=6046, msg='至少需要一个请求参数')
        data, err_txt = MigrateForeignKeyMappingService.post(params=params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
