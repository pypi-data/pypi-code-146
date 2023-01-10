from rest_framework.views import APIView
from ..services.user_service import UserService
from ..services.user_group_tree_service import UserGroupTreeService
from ..utils.custom_response import util_response
from ..utils.model_handle import parse_data


class UserGroupTree(APIView):
    # 在有的框架中会出现传入3个参数的问题，原因不明，可能和两边使用的版本不同有关
    def get(self, request, *args):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            return util_response(err=6045, msg=error_text)
        data, error_text = UserGroupTreeService.group_tree(token_serv['user_id'])
        if not error_text:
            return util_response(data=data)
        return util_response(err=47767, msg=error_text)
