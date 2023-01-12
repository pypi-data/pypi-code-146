from jhc_cf_sdk_test.paths.api_v1_favorites_id.get import ApiForget
from jhc_cf_sdk_test.paths.api_v1_favorites_id.put import ApiForput
from jhc_cf_sdk_test.paths.api_v1_favorites_id.delete import ApiFordelete


class ApiV1FavoritesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
