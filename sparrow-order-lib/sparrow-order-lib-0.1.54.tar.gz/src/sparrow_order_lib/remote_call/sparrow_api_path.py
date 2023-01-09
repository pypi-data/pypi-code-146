# *******************************************************
# 以下部分：涉及 sparrow_core 服务接口
# *******************************************************
# 根据用户id获取用户信息
CORE_USER_INFO_BY_ID_API_PATH = '/api/core_i/user/{}/'
# 根据 app_id 和 user_id 获取 open_id
CORE_USER_OPEN_ID_API_PATH = '/api/core_i/get_openid/'


# *******************************************************
# 以下部分：涉及 sparrow_core_go 服务接口
# *******************************************************
CORE_GO_MEMBER_INFO_API_PATH = '/api/core_go/member'
CORE_GO_I_USER_INFO = '/api/core_go_i/users?user_id={}'

# *******************************************************
# 以下部分：涉及 sparrow_lanyue 服务接口
# *******************************************************
# 批量获取用户信息
LANYUE_I_USER_INFO = '/api/sparrow_lanyue/account_i/bulk_user/'


# *******************************************************
# 以下部分：涉及 sparrow_product 服务接口
# *******************************************************
# 由 导购user_id 查询所在专柜
PRODUCT_SHOP_ID_BY_USER_ID = '/api/sparrow_admin/user/detail/'
# 由 专柜ID 查询所有导购ID
PRODUCT_USER_IDS_BY_SHOP_ID = '/api/shop/shops/{shop_id}/guides/?page_size=100'
# 有 楼层user_id 查询 所有专柜
PRODUCT_SHOP_IDS_FOR_LOUCENG = '/api/shop/stat_data/shop/list/?louceng_user_id={}'
